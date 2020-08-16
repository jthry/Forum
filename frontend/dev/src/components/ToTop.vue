<template>
  <div id="totop">
    <div class="to_top" @click="to_top"><div>&#10132;</div></div>
  </div>
</template>

<script>
export default {
  name: 'ToTop',
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
  opacity: 0;
  transition: all 0.3s;
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
</style>
