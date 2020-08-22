from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from manager.models import Permission
import getpass

class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('username', nargs='+')

  def handle(self, *args, **options):
    username = options['username'][0]
    user = User.objects.filter(username = username)
    if user.exists():
      raise CommandError('User "%s" already exists' % username)
    else:
      password = getpass.getpass('Password:')
      repassword = getpass.getpass('Password (again):')
      if password == '':
        print("Error: Blank passwords aren't allowed.")
      elif password != repassword:
        print("Error: Your passwords didn't match.")
      else:
        try:          
          with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            permission = Permission(
              user = user,
              power = 9999
            )
            permission.save()
            self.stdout.write(self.style.SUCCESS('Successful create administrator "%s"' % username))
        except:
          transaction.rollback()
          raise CommandError('Create failed')
        transaction.commit()
