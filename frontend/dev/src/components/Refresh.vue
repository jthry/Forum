<template>
  <div id="refresh"></div>
</template>
<script>
export default {
  name: 'Refresh',
  beforeCreate() {
    this.$router.replace(this.$route.query.path);
  }
};
</script>
