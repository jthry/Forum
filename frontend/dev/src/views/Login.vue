<template>
  <div id="login">
    <div class="container">
      <div class="title">Log in</div>
      <div class="tip">{{ tip }}</div>
      <div class="icon">
        <font-awesome-icon class="fa" :icon="['fas', 'user']" />
      </div>
      <input type="text" v-model="username" placeholder="Username" />
      <br />
      <div class="icon">
        <font-awesome-icon class="fa" :icon="['fas', 'lock']" />
      </div>
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
  width: 25rem;
  height: 18.75rem;
  text-align: center;
  border-radius: 5px;
  background: white;
  box-shadow: 1px 1px 6px rgb(141, 141, 141);
  margin: 100px auto;
  .title {
    height: 3.125rem;
    color: white;
    text-align: left;
    text-indent: 1.25rem;
    font-size: 1.25rem;
    line-height: 3.125rem;
    border-radius: 5px 5px 0 0;
    background: rgba(0, 0, 0, 0.7);
  }
  .tip {
    height: 1.875rem;
    font-size: 0.875rem;
    line-height: 1.875rem;
    color: red;
  }
  .icon {
    display: inline-block;
    width: 26px;
    height: 30px;
    color: white;
    font-size: 16px;
    line-height: 29px;
    text-align: center;
    background: rgb(100, 100, 100);
    padding-left: 2px;
    vertical-align: top;
  }
  input {
    width: 12.5rem;
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
    width: 5rem;
    color: white;
    border-radius: 3px;
    margin: 0 calc(15px + 0.625rem);
    font-size: 0.875rem;
    background: rgb(102, 102, 102);
    padding: 5px 0.3125rem;
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
