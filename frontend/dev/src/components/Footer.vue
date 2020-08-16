<template>
  <div id="footer">
    <div class="copy_container">
      <span class="copyright">©{{ thisYear }} XX. All rights reserved.</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'appFooter',
  data() {
    return {
      thisYear: ''
    };
  },
  computed: {},
  methods: {},
  created() {
    this.thisYear = this.$store.state.now.getFullYear();
  }
};
</script>

<style scoped>
#footer {
  width: 100%;
  height: 50px;
  color: white;
  text-align: center;
  background: rgba(122, 122, 122);
  box-shadow: 0px 0px 6px rgb(80, 80, 80);
}
.copy_container {
  display: inline-block;
  height: 100%;
}
.copy_container .copyright::after {
  content: '';
  display: inline-block;
  height: 100%;
  visibility: hidden;
  vertical-align: middle;
}
</style>
