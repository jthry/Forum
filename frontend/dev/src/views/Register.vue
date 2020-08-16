<template>
  <div id="register">
    <div class="container">
      <div class="title">Sign up</div>
      <input type="text" v-model="username" placeholder="Username" />
      <div class="tip">{{ username_tip }}</div>
      <input type="password" v-model="password" placeholder="Password" />
      <div class="tip">{{ password_tip }}</div>
      <input type="password" v-model="repassword" placeholder="Confirm password" />
      <div class="tip">{{ repassword_tip }}</div>
      <div class="button" @click="register">Sign up</div>
      <router-link class="button" to="/login" tag="div">Back</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      repassword: ''
    };
  },
  computed: {
    username_tip: function() {
      var len = this.username.length;
      var bt = 0;
      if (len >= 2 && len <= 16) {
        for (var i = 0; i < len; i++) {
          var c = this.username.charAt(i);
          if (/[A-Za-z0-9\u0080-\u00ff]/.test(c)) bt++;
          else if (/[\u00ff-\u9fa5]/.test(c)) bt += 2;
          else return 'Only supports words or numbers';
        }
        if (bt >= 4 && bt <= 16) return '';
        else return 'Must be 4-16 words or numbers';
      } else if (len == 0) return '';
      else return 'Must be 4-16 words or numbers';
    },
    password_tip: function() {
      var len = this.password.length;
      if (len >= 6 && len <= 20) {
        if (
          /^(?=[0-9]+[^0-9]|[^0-9]+[0-9]|[a-zA-Z]+[^a-zA-Z]|[^a-zA-Z]+[a-zA-Z])[\x21-\x7f]{6,20}$/.test(this.password)
        ) {
          return '';
        } else {
          return 'At least two of words, numbers or symbols';
        }
      } else if (len == 0) return '';
      else return 'Length must be 6 to 20';
    },
    repassword_tip: function() {
      if (this.repassword == '' || this.password == this.repassword) return '';
      else return 'Please enter the same password';
    }
  },
  methods: {
    register: function() {
      if (
        this.username_tip == '' &&
        this.password_tip == '' &&
        this.repassword_tip == '' &&
        this.username != '' &&
        this.password != ''
      ) {
        if (this.$store.state.btn_switch) {
          this.$store.dispatch('btn_sleep');
          this.$axios
            .post('user/register', {
              username: this.username,
              password: this.password
            })
            .then(response => {
              if (response.data.code == 1) {
                this.$router.push({ path: '/login' });
              } else {
                alert('Register failed');
              }
            })
            .catch(() => {
              alert('Register failed');
            });
        }
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
    margin-bottom: 30px;
  }
  .tip {
    width: 200px;
    height: 20px;
    color: red;
    font-size: 14px;
    text-align: left;
    margin: auto;
    white-space: nowrap;
  }
  input {
    width: 200px;
    height: 24px;
    color: rgb(51, 51, 51);
    font-size: 16px;
    text-indent: 5px;
    border: 2px solid rgb(100, 100, 100);
    outline: 0;
  }
  input:focus {
    box-shadow: 0px 0px 0px 1px rgb(100, 100, 100), 0px 0px 10px 2px rgb(100, 100, 100);
  }
  .button {
    display: inline-block;
    width: 80px;
    color: white;
    font-size: 14px;
    border-radius: 3px;
    background: rgb(102, 102, 102);
    margin: 0 10px;
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
