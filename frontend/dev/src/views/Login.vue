<template>
  <div id="login">
    <div class="container">
      <div class="title">Log in</div>
      <div class="tip">{{ tip }}</div>
      <font-awesome-icon class="fa" :icon="['fas', 'user']" />
      <input type="text" v-model="username" placeholder="Username" />
      <br />
      <font-awesome-icon class="fa" :icon="['fas', 'lock']" />
      <input type="password" v-model="password" placeholder="Password" />
      <br />
      <div class="button" @click="login">Log in</div>
      <router-link class="button" to="/register" tag="div">Sign up</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      tip: ''
    };
  },
  methods: {
    login: function() {
      if (this.username == '') this.tip = 'Please enter username';
      else if (this.password == '') this.tip = 'Please enter password';
      else {
        this.$axios
          .post('user/login', {
            username: this.username,
            password: this.password
          })
          .then(response => {
            if (response.data.code == 1) {
              this.$store.commit('change_login_state', true);
              this.$store.commit('set_username', this.username);
              if (response.data.power) {
                this.$store.commit('set_power', response.data.power);
                this.$store.commit('set_area', response.data.area);
              }
              this.$router.push({ path: '/forum' });
            } else {
              this.tip = 'Username or Password error';
            }
          })
          .catch(() => {
            this.tip = 'Login failed';
            this.$store.commit('change_login_state', false);
          });
      }
    }
  }
};
</script>

<style lang="less" scoped>
.container {
  width: 400px;
  height: 300px;
  text-align: center;
  border-radius: 5px;
  background: white;
  box-shadow: 1px 1px 6px rgb(141, 141, 141);
  margin: 100px auto;
  .title {
    height: 50px;
    color: white;
    text-align: left;
    text-indent: 20px;
    font-size: 20px;
    line-height: 50px;
    border-radius: 5px 5px 0 0;
    background: rgba(0, 0, 0, 0.7);
  }
  .tip {
    height: 30px;
    font-size: 14px;
    line-height: 30px;
    color: red;
  }
  .fa {
    color: white;
    background: rgb(100, 100, 100);
    padding: 7px 6px 7px 8px;
    vertical-align: top;
  }
  input {
    width: 200px;
    height: 24px;
    color: rgb(51, 51, 51);
    font-size: 16px;
    text-indent: 5px;
    border: 2px solid rgb(100, 100, 100);
    outline: 0;
    margin-bottom: 20px;
  }
  input:focus {
    box-shadow: 0px 0px 0px 1px rgb(100, 100, 100), 0px 0px 10px 2px rgb(100, 100, 100);
  }
  .button {
    display: inline-block;
    width: 80px;
    color: white;
    border-radius: 3px;
    margin: 0 25px;
    font-size: 14px;
    background: rgb(102, 102, 102);
    padding: 5px;
    cursor: pointer;
    transition: background 0.2s, color 0.4s;
  }
  .button:hover {
    background: rgb(134, 134, 134);
    color: rgb(39, 39, 39);
  }
  .button:active {
    background: rgb(163, 163, 163);
    color: rgb(80, 80, 80);
  }
}
</style>
