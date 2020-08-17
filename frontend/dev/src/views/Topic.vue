<template>
  <!-- eslint-disable prettier/prettier -->
  <div id="topic">
    <div class="topic_container">
      <div class="topic">{{ topic.topic }}</div>
      <div class="container" v-for="(item, index) in posts" :key="item.post_num">
        <div class="poster_container">
          <div class="poster" :class="creator(item.is_creator)">{{ item.poster }}</div>
          <div class="profile">
            <font-awesome-icon :icon="['fas', 'user']" />
          </div>
        </div>
        <div class="post_container">
          <div class="detail clearfix">
            <div class="date">{{ time_format_post(item.date) }}</div>
            <div class="post_num">#{{ item.post_num }}</div>
            <div class="finish button" title="finish" @click="update(index, item.post_num)" v-if="is_poster(item.poster)" v-show="is_edit(index)">
              <font-awesome-icon :icon="['fas', 'check']" />
            </div>
            <div class="delete button" title="delete" @click="del(index,item.post_num)" v-if="is_poster(item.poster)&&not_1(item.post_num)" v-show="!is_edit(index)">
              <font-awesome-icon :icon="['fas', 'trash-alt']" />
            </div>
            <div class="edit button" title="edit" @click="edit(index,item.post)" v-if="is_poster(item.poster)" v-show="!is_edit(index)">
              <font-awesome-icon :icon="['fas', 'pencil-alt']" />
            </div>
            <div class="cancel button" title="cancel" @click="cancel" v-if="is_poster(item.poster)" v-show="is_edit(index)">
              <font-awesome-icon :icon="['fas', 'times']" />
            </div>
          </div>
          <div class="post">
            <div v-show="!is_edit(index)">{{ item.post }}</div>
            <text-edit class="text_edit" :text_first="edit_content" @change_text="change_text" v-if="is_edit(index)"></text-edit>
          </div>
        </div>
      </div>
    </div>
    <page class="page_container" :current_page="page" :max_page="max_page" @page_turn="page_turn"></page>
    <post class="post_container" is_topic="" :board_num="board_num" :topic_num="topic_num"></post>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:8000/';
axios.defaults.withCredentials = true;

function get_data(to, from, next, vm_exist) {
  let path = to.path.split('/');
  let board_num = path[path.length - 2];
  let [topic_num, page] = path[path.length - 1].split('-');

  // eslint-disable-next-line prettier/prettier
  if (
    /^[1-9][0-9]*$/.test(board_num) &&
    /^[1-9][0-9]*$/.test(topic_num) &&
    (page == undefined || /^[1-9][0-9]*$/.test(page))
  ) {
    page = page || 1;
    let vm;
    let get_vm = v => (vm = v);

    axios
      .get('/forum/' + board_num + '/' + topic_num, {
        params: {
          page: page
        }
      })
      .then(response => {
        vm = vm || vm_exist;
        set_data(response, vm, page, topic_num, board_num);
      });

    next(vm => {
      get_vm(vm);
    });
  } else {
    next('/404');
  }
}

function set_data(response, vm, page, topic_num, board_num) {
  let topic = response.data.topic_information;
  let posts = response.data.post_data;

  vm.board_num = board_num || vm.board_num;
  vm.topic_num = topic_num || vm.topic_num;
  vm.page = Number(page) || vm.page;
  let max = topic.post_sum;
  max = Math.ceil(max / 20);
  max = max ? max : 1;
  vm.max_page = max;
  vm.$set(vm, 'topic', topic);
  vm.$set(vm, 'posts', posts);
}

export default {
  name: 'Topic',
  data() {
    return {
      topic: '',
      posts: '',
      edit_content: '',
      edit_index: '',
      board_num: '',
      topic_num: '',
      page: 1,
      max_page: 1
    };
  },
  components: {
    post: () => import('@/components/Post'),
    page: () => import('@/components/Page'),
    textEdit: () => import('@/components/TextEdit')
  },
  methods: {
    change_text(text) {
      this.edit_content = text;
    },
    creator(is_creator) {
      if (is_creator) return 'creator';
    },
    is_poster(poster) {
      return poster == this.$store.state.username;
    },
    not_1(post_num) {
      return post_num !== 1;
    },
    is_edit(index) {
      return index === this.edit_index;
    },
    edit(index, post) {
      if (this.edit_index === '') {
        this.edit_index = index;
        this.edit_content = post;
      }
    },
    cancel() {
      if (this.edit_index !== '') {
        this.edit_index = '';
        this.edit_content = '';
      }
    },
    update(index, post_num) {
      if (this.$store.state.btn_switch) {
        if (this.edit_index !== '') {
          if (this.edit_content == this.posts[0]['post']) {
            this.edit_index = '';
            this.edit_content = '';
          } else {
            this.$store.dispatch('btn_sleep');
            this.$axios
              .post('/forum/updatepost', {
                board_num: this.board_num,
                topic_num: this.topic_num,
                page: this.page,
                post_num: post_num,
                post: this.edit_content
              })
              .then(response => {
                this.edit_index = '';
                this.edit_content = '';
                set_data(response, this);
              })
              .catch(() => {
                this.edit_index = '';
                this.edit_content = '';
              });
          }
        }
      }
    },
    del(index, post_num) {
      if (this.$store.state.btn_switch) {
        this.$store.dispatch('btn_sleep');
        let page = this.page;
        if (this.posts.length == 1 && this.page != 1) {
          page = this.page - 1;
        }
        this.$axios
          .post('/forum/deletepost', {
            board_num: this.board_num,
            topic_num: this.topic_num,
            page: this.page,
            post_num: post_num
          })
          .then(response => {
            if (response.status == 200) {
              set_data(response, this, page);
            }
          });
      }
    },
    page_turn(page) {
      let path = '/forum/' + this.board_num + '/' + this.topic_num + '-' + page;
      this.$router.push({ path: path });
    },
    time_format_post(date) {
      date = new Date(date);
      let now = this.$store.state.now;
      let time = now - date;
      let today = now - (now % (24 * 60 * 60 * 1000));
      let yesterday = today - 24 * 60 * 60 * 1000;
      let hours = date.getHours();
      let minutes = date.getMinutes();
      minutes = minutes < 10 ? '0' + minutes : minutes;

      if (time < 60000) {
        return 'A moment ago';
      } else if (date >= yesterday && date < today) {
        return 'Yesterday at ' + hours + ':' + minutes;
      } else if (time < 60 * 60 * 1000 && time >= 60 * 1000) {
        return Math.floor(time / 60000) + ' minutes ago';
      } else if (time < 24 * 60 * 60 * 1000 && time >= 60 * 60 * 1000) {
        return 'Today at ' + hours + ':' + minutes;
      } else {
        return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + hours + ':' + minutes;
      }
    }
  },
  beforeRouteEnter(to, from, next) {
    get_data(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    get_data(to, from, next, this);
  }
};
</script>

<style lang="less" scoped>
.clearfix::after {
  content: '';
  display: block;
  clear: both;
  height: 0;
  width: 0;
  visibility: hidden;
}
#topic {
  padding: 3%;
  .topic_container {
    box-shadow: 0px 0px 5px rgb(80, 80, 80);
    margin-bottom: 5px;
    .topic {
      color: white;
      font-size: 24px;
      border-bottom: 2px solid rgb(196, 196, 196);
      background: rgb(155, 155, 155);
      background-image: linear-gradient(to right, rgb(120, 120, 120), rgb(180, 180, 180), rgb(200, 200, 200));
      padding: 10px;
    }
    .container {
      display: flex;
      border-bottom: 2px solid rgb(196, 196, 196);
      background: white;
      .poster_container {
        width: 150px;
        text-align: center;
        border-right: 1px solid rgb(211, 211, 211);
        background: rgb(248, 248, 248);
        .poster {
          color: rgb(64, 64, 255);
          border-bottom: 1px solid rgb(211, 211, 211);
          padding: 3px;
        }
        .creator {
          color: rgb(255, 64, 64);
        }
        .profile {
          width: 100px;
          height: 100px;
          color: white;
          font-size: 70px;
          text-align: center;
          line-height: 100px;
          background: rgb(203, 223, 255);
          margin: 10px auto;
        }
      }
      .post_container {
        flex: 1;
        .detail {
          color: rgb(136, 136, 136);
          border-bottom: 1px solid rgb(211, 211, 211);
          padding: 3px;
          .date {
            display: inline-block;
          }
          .post_num {
            float: right;
            margin-right: 10px;
          }
          .button {
            float: right;
            width: 16px;
            font-size: 16px;
            text-align: center;
            margin-right: 10px;
            cursor: pointer;
          }
        }
        .post {
          min-height: 200px;
          padding: 3px;
          .text_edit {
            min-height: 200px;
          }
        }
      }
    }
  }
}
</style>
