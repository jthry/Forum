import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faUser,
  faLock,
  faComments,
  faComment,
  faTrashAlt,
  faPencilAlt,
  faCheck,
  faTimes,
  faBars,
  faCaretDown,
  faPlus
} from '@fortawesome/free-solid-svg-icons';

Vue.config.productionTip = false;
Vue.config.devtools = true;

Vue.prototype.$axios = axios;
axios.defaults.baseURL = 'http://127.0.0.1:8000/';
axios.defaults.withCredentials = true;

// axios.get('user/csrf').catch(() => {});
// axios.interceptors.request.use(config => {
//   var djangoCookie = getCookie('csrftoken')
//   config.headers['X-CSRFToken'] = djangoCookie
//   return config
// }, error => {
//   return Promise.reject(error);
// })

(function() {
  //The development environment to verify identity
  axios.post('/getlogincookies', { code: 1 }).then(() => {
    (function() {
      if (getCookie('isLogin') == 1) {
        store.commit('change_login_state', true);
      }
      let username = getCookie('username');
      if (username) {
        store.commit('set_username', username);
      }
      let power = getCookie('power');
      if (power) {
        store.commit('set_power', power);
      }
      let area = getCookie('area');
      if (area) {
        store.commit('set_area', area);
      }
      delCookie('isLogin');
      delCookie('username');
      delCookie('power');
      delCookie('area');
    })();

    router.beforeEach((to, from, next) => {
      store.commit('set_scroll_top', 0);
      if (!to.meta.not_login && store.state.login_state) {
        next();
      } else if (to.meta.not_login && !store.state.login_state) {
        next();
      } else if (to.path == '/' && store.state.login_state) {
        next('/forum');
      } else {
        next(from);
      }
    });

    library.add(
      faUser,
      faLock,
      faComments,
      faComment,
      faTrashAlt,
      faPencilAlt,
      faCheck,
      faTimes,
      faBars,
      faCaretDown,
      faPlus
    );
    Vue.component('font-awesome-icon', FontAwesomeIcon);

    Vue.mixin({
      methods: {
        time_format(date) {
          if (date) {
            date = new Date(date);
            let now = this.$store.state.now;
            let time = now - date;
            let today = now - (now % (24 * 60 * 60 * 1000));
            let yesterday = today - 24 * 60 * 60 * 1000;

            if (time < 60000) {
              return 'A moment ago';
            } else if (date >= yesterday && date < today) {
              let hours = date.getHours();
              let minutes = date.getMinutes();
              minutes = minutes < 10 ? '0' + minutes : minutes;
              return 'Yesterday at ' + hours + ':' + minutes;
            } else if (time < 60 * 60 * 1000 && time >= 60 * 1000) {
              return Math.floor(time / 60000) + ' minutes ago';
            } else if (time < 24 * 60 * 60 * 1000 && time >= 60 * 60 * 1000) {
              return Math.floor(time / 3600000) + ' hours ago';
            } else if (date >= today - 7 * 24 * 60 * 60 * 1000 && date < yesterday) {
              return Math.ceil((today - date) / (24 * 60 * 60 * 1000)) + ' days ago';
            } else {
              return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
            }
          } else {
            return '';
          }
        }
      }
    });

    new Vue({
      router,
      store,
      render: h => h(App)
    }).$mount('#app');

    function getCookie(name) {
      let reg = new RegExp('(?<=(^| )' + name + '=).+?(?=;|$)');
      let cookie = document.cookie.match(reg) || [null];
      cookie = cookie[0] !== null ? JSON.parse(JSON.parse(cookie[0])) : null;
      return cookie;
    }

    function delCookie(name) {
      document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    }
  });
})();
