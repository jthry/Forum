# Forum

A simple forum based on Vue.js and Django

## Technology stack

+ vue.js
+ vuex
+ vue-router
+ axios
+ django

## Installation

### Prerequisites

First of all, you need install Node.js, Python and Mysql

### Get the code

```
git clone https://github.com/jthry/Forum.git
```

### Configuration

Create a new database  
Then create a new file config.py in backend/backend, add the following content

`SECRET_KEY = 'a secret key'`  
For example, '000000'  
```
NAME = 'database name'  
USER = 'database user'  
PASSWORD = 'database password'  
HOST = 'database host'  
PORT = 'database port'  
```

### Frontend

```
npm install
npm run build
```

### Backend

```
pip3 install -r requirements.txt
python manage.py makemigrations --empty user
python manage.py makemigrations --empty forum
python manage.py makemigrations forum
python manage.py migrate
```

### Insert initial data in database

```
insert into forum_boards values (1, 'test1', 100, null, null, null)
insert into forum_boards values (2, 'test2', 101, 0, 0, null)
```

### Run

```
python manage.py runserver
```
