<template>
  <div id="app">
    <app-header v-if="this.$store.state.login_state"></app-header>
    <router-view class="view" />
    <app-footer v-if="this.$store.state.login_state"></app-footer>
  </div>
</template>

<script>
export default {
  components: {
    appHeader: () => import('@/components/Header'),
    appFooter: () => import('@/components/Footer')
  },
  methods: {
    set_scroll_top() {
      this.$store.commit('set_scroll_top');
    }
  },
  beforeMount() {
    this.$store.dispatch('update_time');
  },
  mounted() {
    window.addEventListener('scroll', this.set_scroll_top);
  },
  destroyed() {
    window.removeEventListener('scroll', this.set_scroll_top);
  }
};
</script>

<style lang="less" scoped>
#app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  word-break: break-word;
  .view {
    flex: 1;
    padding: 5%;
  }
}
</style>
