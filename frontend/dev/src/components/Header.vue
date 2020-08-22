<template>
  <div id="header">
    <div class="header clearfix" :class="header_scroll">
      <div class="logo_container">
        <router-link to="/" class="logo" tag="div">Forum</router-link>
      </div>
      <div class="user_container">
        <div class="user">{{ username }}</div>
        <div class="user_menu">
          <div @click="change_password">Change password</div>
          <div @click="logout">Logout</div>
        </div>
      </div>
      <change-password :is_change="is_change"></change-password>
      <to-top></to-top>
    </div>
    <div class="fixed"></div>
  </div>
</template>

<script>
export default {
  name: 'appHeader',
  data() {
    return {
      username: this.$store.state.username,
      is_change: 0
    };
  },
  components: {
    changePassword: () => import('@/components/ChangePassword'),
    toTop: () => import('@/components/ToTop')
  },
  computed: {
    header_scroll() {
      let scroll_top = this.$store.state.scroll_top;
      if (scroll_top > 55) {
        return 'header_scroll';
      } else {
        return '';
      }
    }
  },
  methods: {
    change_password() {
      this.is_change = this.is_change ? 0 : 1;
    },
    logout() {
      this.$axios.post('/user/logout').then(response => {
        if (response.data.code == 1) {
          this.$store.commit('change_login_state', false);
          this.$store.commit('set_username', '');
          this.$router.push({ path: '/login' });
        }
      });
    }
  }
};
</script>

<style lang="less" scoped>
.header {
  width: 100%;
  height: 49px;
  color: white;
  font-size: 20px;
  text-align: center;
  background-image: linear-gradient(rgba(60, 60, 60, 0.9), rgba(30, 30, 30, 0.9));
  box-shadow: 0px 3px 6px rgba(30, 30, 30, 0.9);
  padding: 3px 0;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  transition: padding 0.3s;
  .logo_container {
    float: left;
    width: 150px;
    height: 100%;
    .logo {
      font-size: 36px;
      text-decoration: none;
      cursor: pointer;
    }
  }
  .user_container {
    display: flex;
    justify-content: center;
    align-items: center;
    float: right;
    width: 100px;
    height: 100%;
    position: relative;
    .user {
      flex: 1;
      font-size: 18px;
      line-height: 22px;
      padding-bottom: 2px;
    }
    .user_menu {
      width: 100%;
      max-height: 0;
      overflow: hidden;
      margin: auto;
      box-sizing: border-box;
      position: absolute;
      top: 49px;
      transition: max-height 0.5s;
      > div {
        font-size: 14px;
        border: 1px solid #aaa;
        background: rgba(0, 0, 0, 0.7);
        padding: 5px 0;
        cursor: pointer;
      }
      > div:hover {
        background: rgba(56, 56, 56, 0.7);
      }
    }
  }
  .user_container:hover {
    background: rgb(60, 60, 60);
    .user_menu {
      max-height: 100px;
    }
  }
  .user_container:hover .user_menu {
    display: block;
  }
}
.header_scroll {
  background: rgba(30, 30, 30, 0.7);
  box-shadow: none;
  padding: 0;
}
.fixed {
  height: 55px;
  visibility: hidden;
}

.clearfix::after {
  content: '';
  display: block;
  clear: both;
  width: 0;
  height: 0;
  visibility: hidden;
}
</style>
