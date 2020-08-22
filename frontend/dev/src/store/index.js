import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    login_state: false,
    username: '',
    now: '',
    scroll_top: 0,
    btn_switch: true,
    power: 0,
    area: []
  },
  mutations: {
    change_login_state(state, value) {
      state.login_state = value;
    },
    set_username(state, value) {
      state.username = value;
    },
    update_time(state) {
      state.now = new Date();
    },
    set_scroll_top(state, value = null) {
      let scroll_top = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
      if (state.scroll_top != scroll_top) {
        state.scroll_top = scroll_top;
      }
      if (scroll_top != value && value != null) {
        document.documentElement.scrollTop = value;
        window.pageYOffset = value;
        document.body.scrollTop = value;
      }
    },
    change_btn_switch(state, value) {
      state.btn_switch = value;
    },
    set_power(state, value) {
      state.power = value;
    },
    set_area(state, value) {
      state.area = value;
    }
  },
  actions: {
    update_time({ commit }) {
      commit('update_time');
      setInterval(() => {
        commit('update_time');
      }, 1000);
    },
    smooth_scroll({ commit }, to) {
      let scroll_top = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
      let step = (scroll_top - to) / 25;
      let times = 25;
      let interval = setInterval(() => {
        scroll_top = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
        // eslint-disable-next-line prettier/prettier
        if (
          (scroll_top - to <= step && step > 0) ||
          (scroll_top - to >= step && step < 0) ||
          times <= 1
        ) {
          step = scroll_top - to;
          clearInterval(interval);
        }
        times--;
        commit('set_scroll_top', scroll_top - step);
      }, 20);
    },
    btn_sleep({ commit }) {
      commit('change_btn_switch', false);
      setTimeout(() => {
        commit('change_btn_switch', true);
      }, 1000);
    }
  }
});
