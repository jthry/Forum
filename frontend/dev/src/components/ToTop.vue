<template>
  <div id="totop">
    <div class="to_top" :class="cls" @click="to_top"><div>&#10132;</div></div>
  </div>
</template>

<script>
export default {
  name: 'ToTop',
  data() {
    return {
      delete: 'delete'
    }
  },
  computed: {
    cls() {
      let scroll_top = this.$store.state.scroll_top;
      if (scroll_top > 200) {
        return 'show';
      } else {
        return '' + this.delete;
      }
    }
  },
  watch: {
    cls() {
      if (this.cls == '') {
        setTimeout(() => {
          if (this.cls == '') {
            this.delete = 'delete';
          }
        }, 300);
      }
      if (this.cls == 'show') {
        this.delete = '';
      }
    }
  },
  methods: {
    to_top() {
      this.$store.dispatch('smooth_scroll', 0);
    }
  }
};
</script>

<style lang="less" scoped>
.to_top {
  width: 30px;
  height: 30px;
  color: rgba(30, 30, 30, 0.7);
  font-size: 26px;
  border: 2px solid rgba(30, 30, 30, 0.7);
  border-radius: 50%;
  position: fixed;
  bottom: 10px;
  right: 10px;
  overflow: hidden;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
  > div {
    margin: -3px 0 0 -3px;
    transform: rotate(-90deg);
  }
}
.to_top:hover {
  color: black;
  border: 2px solid black;
}
.delete {
  width: 0;
  height: 0;
  border: none;
}
.show {
  opacity: 1;
}
</style>
