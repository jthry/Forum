<template>
  <div id="page">
    <div class="page" :class="current(page)" @click="page_turn(page)" v-for="page in page_arr" :key="page">
      {{ page }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Page',
  props: {
    current_page: Number,
    max_page: Number
  },
  data() {
    return {
      previous_page: '<',
      next_page: '>'
    };
  },
  computed: {
    page_arr() {
      let arr = [];
      if (this.current_page != 1) {
        arr.push(this.previous_page);
      }
      arr.push(1);
      if (this.current_page > 6 && this.max_page > 11) {
        arr.push('...');
      }

      let page = this.current_page > 6 ? this.current_page - 4 : 2;
      page = page > this.max_page - 9 ? this.max_page - 9 : page;
      let len = this.max_page > 10 ? 8 : this.max_page - 3;
      for (let i = 0; i <= len; i++) {
        arr.push(page + i);
      }

      if (this.max_page - this.current_page > 5 && this.max_page > 11) {
        arr.push('...');
      }
      if (this.max_page != 1) {
        arr.push(this.max_page);
      }
      if (this.current_page != this.max_page) {
        arr.push(this.next_page);
      }

      return arr;
    }
  },
  methods: {
    current(page) {
      if (page == this.current_page) return 'current_page';
    },
    page_turn(page) {
      if (page == this.previous_page) {
        this.$emit('page_turn', this.current_page - 1);
      } else if (page == this.next_page) {
        this.$emit('page_turn', this.current_page + 1);
      } else if (page == '...') {
        return;
      } else if (page != this.current_page) {
        this.$emit('page_turn', page);
      }
    }
  }
};
</script>

<style lang="less" scoped>
#page {
  .page {
    display: inline-block;
    min-width: 26px;
    height: 30px;
    font-size: 14px;
    text-align: center;
    line-height: 30px;
    border: 1px solid rgb(172, 172, 172);
    background: white;
    box-shadow: 0px 0px 3px rgb(130, 130, 130);
    margin: 5px 2px;
    padding: 0 2px;
    cursor: pointer;
    transition: background 0.3s, color 0.3s;
  }
  .page:hover {
    color: white;
    background: rgb(88, 88, 88);
  }
  .page:active {
    background: rgb(151, 151, 151);
  }
  :first-child {
    margin-left: 0;
  }
  :last-child {
    margin-right: 0;
  }
  .current_page {
    color: white;
    background: rgb(88, 88, 88);
  }
}
</style>
