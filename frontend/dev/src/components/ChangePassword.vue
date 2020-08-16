<template>
  <div id="changepassword">
    <div class="password_background" v-if="show">
      <div class="password_window">
        <div class="tip">{{ tip }}</div>
        <input type="password" v-model="old_password" placeholder="Old password" />
        <input type="password" v-model="new_password" placeholder="New password" />
        <input type="password" v-model="repassword" placeholder="Confirm password" />
        <br />
        <div class="button" @click="submit_password">OK</div>
        <div class="button" @click="cancel_change">Cancel</div>
      </div>
    </div>
    <div class="hidden">{{ watch_is_change }}</div>
  </div>
</template>

<script>
export default {
  name: 'ChangePassword',
  props: ['is_change'],
  data() {
    return {
      tip: '',
      old_password: '',
      new_password: '',
      repassword: '',
      show: false,
      can_show: false
    };
  },
  computed: {
    watch_is_change() {
      if (this.can_show) {
        this.is_show();
      }
      return this.is_change;
    }
  },
  methods: {
    is_show() {
      this.show = true;
    },
    submit_password() {
      if (
        this.new_password != '' &&
        this.old_password != '' &&
        this.new_password == this.repassword &&
        this.new_password != this.old_password
      ) {
        this.$axios
          .post('/user/changepassword', {
            old_password: this.old_password,
            new_password: this.new_password
          })
          .then(response => {
            if (response.data.code == 1) {
              this.$store.commit('changeLoginState', false);
              this.$store.commit('setUsername', '');
              this.$router.push({ path: '/login' });
            }
            this.cancel_change();
          })
          .catch(() => {
            this.cancel_change();
          });
      } else {
        this.tip = 'Fail';
      }
    },
    cancel_change() {
      this.tip = '';
      this.old_password = '';
      this.new_password = '';
      this.repassword = '';
      this.show = false;
    }
  },
  beforeUpdate() {
    this.can_show = true;
  }
};
</script>

<style lang="less" scoped>
.password_background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(100, 100, 100, 0.5);
  .password_window {
    width: 280px;
    height: 180px;
    background: #fff;
    margin: auto;
    margin-top: 100px;
    padding: 30px;
    .tip {
      display: inline-block;
      width: 180px;
      height: 20px;
      font-size: 14px;
      text-align: left;
      line-height: 20px;
      color: red;
    }
    input {
      width: 180px;
      margin: 3px;
    }
    .button {
      display: inline-block;
      width: 50px;
      font-size: 14px;
      border: 1px solid #aaa;
      background: #ddd;
      margin: 5px 15px;
      padding: 1px 3px;
      cursor: pointer;
    }
    .button:active {
      background: #bbb;
    }
  }
}
.hidden {
  width: 0;
  height: 0;
  font-size: 0;
  visibility: hidden;
}
</style>
