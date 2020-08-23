<template>
  <div id="manage" v-if="is_manage">
    <div class="icon" :class="icon_active" @click="active" v-if="!show_add">
      <font-awesome-icon :icon="['fas', 'caret-down']" />
    </div>
    <div class="menu" :class="menu_active" v-if="!show_add">
      <div class="delete" v-if="is_delete" @click="del">Delete</div>
      <div class="promote" v-if="is_promote" @click="promote">Promote to moderator</div>
    </div>
    <div class="add_board" v-if="show_add" @click="open_add_window">
      <font-awesome-icon :icon="['fas', 'plus']" />
    </div>
    <div class="add_window" :class="add_open" v-if="show_add">
      <input type="text" v-model="container_name" placeholder="Container name" />
      <input type="text" v-model="board_name" placeholder="Board name" />
      <br />
      <div class="button" @click="submit_add">OK</div>
      <div class="button" @click="cancel_add">Cancel</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Manage',
  props: ['power', 'board_num', 'topic_num', 'post_num', 'add_board'],
  data() {
    return {
      icon_active: '',
      menu_active: '',
      add_open: '',
      container_name: '',
      board_name: ''
    };
  },
  computed: {
    is_delete() {
      if (this.$store.state.power > this.power && this.post_num != 1) return 'is_delete';
      else return '';
    },
    is_promote() {
      let power = this.$store.state.power;
      if (power > 1000 && this.power == 0 && this.post_num) return 'is_promote';
      else return '';
    },
    is_manage() {
      if (this.is_delete == '' && this.is_promote == '' && this.show_add == '') return '';
      else return 'is_manage';
    },
    show_add() {
      if (this.$store.state.power > this.power && this.add_board == true) return 'show_add';
      else return '';
    }
  },
  methods: {
    active() {
      if (this.icon_active == '') this.icon_active = 'icon_active';
      else this.icon_active = '';
      if (this.menu_active == '') this.menu_active = 'menu_active';
      else this.menu_active = '';
    },
    del() {
      this.$axios
        .post('/manager/delete', {
          board_num: this.board_num,
          topic_num: this.topic_num,
          post_num: this.post_num
        })
        .then(response => {
          if (response.data.code == 1) {
            this.$router.push({ path: '/refresh', query: { path: this.$route.fullPath } });
          }
        })
        .catch(() => {});
    },
    promote() {
      this.$axios
        .post('/manager/promote', {
          board_num: this.board_num,
          topic_num: this.topic_num,
          post_num: this.post_num
        })
        .then(response => {
          if (response.data.code == 1) {
            this.$router.push({ path: '/refresh', query: { path: this.$route.fullPath } });
          }
        })
        .catch(() => {});
    },
    open_add_window() {
      this.add_open = 'add_open';
    },
    submit_add() {
      let data = {};
      if (this.container_name != '') {
        data['container_name'] = this.container_name;
        if (this.board_name != '') data['board_name'] = this.board_name;
        this.$axios
          .post('/manager/add', data)
          .then(response => {
            if (response.data.code == 1) {
              this.$router.push({ path: '/refresh', query: { path: this.$route.fullPath } });
            }
          })
          .catch(() => {});
      }
    },
    cancel_add() {
      this.add_open = '';
    }
  }
};
</script>

<style lang="less" scoped>
#manage {
  position: absolute;
  .icon {
    width: 30px;
    height: 30px;
    color: rgb(0, 0, 0);
    font-size: 20px;
    text-align: center;
    line-height: 30px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    position: absolute;
    top: 0;
    left: 0;
    z-index: 150;
    transform: translate(-50%, -50%);
    transition: all 0.3s;
    cursor: pointer;
  }
  .icon:hover {
    background: rgb(255, 255, 255);
    box-shadow: 0px 0px 3px black;
  }
  .icon_active {
    background: rgb(255, 255, 255);
    box-shadow: 0px 0px 3px black;
    transform: translate(-50%, -50%) rotate(-90deg);
  }
  .menu {
    max-height: 0;
    color: white;
    text-align: center;
    white-space: nowrap;
    background: rgba(0, 0, 0, 0.7);
    transition: max-height 0.5s;
    overflow: hidden;
    position: absolute;
    top: 0;
    left: 15px;
    z-index: 200;
    cursor: pointer;
    > div {
      border: 1px solid white;
      padding: 3px;
    }
  }
  .menu_active {
    max-height: 100px;
  }
  .add_board {
    width: 90vw;
    height: 30px;
    color: rgb(80, 80, 80);
    font-size: 22px;
    text-align: center;
    background: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    transition: background 0.3s;
  }
  .add_board:hover {
    background: rgba(255, 255, 255, 0.7);
  }
  .add_window {
    display: none;
    width: 200px;
    height: 100px;
    text-align: center;
    background: white;
    box-shadow: 0px 0px 5px black;
    padding: 5px;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    input {
      width: 180px;
      margin: 3px;
    }
    .button {
      display: inline-block;
      width: 50px;
      font-size: 14px;
      border: 1px solid #aaa;
      background: #ddd;
      margin: 5px 15px;
      padding: 1px 3px;
      cursor: pointer;
    }
    .button:active {
      background: #bbb;
    }
  }
  .add_open {
    display: block;
  }
}
</style>
