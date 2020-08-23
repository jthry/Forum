<template>
  <div id="board">
    <div class="board_container">
      <div class="head">
        <div class="head_name">{{ head.name }}</div>
        <div class="topic_sum">Topics:{{ head.topic_sum }}</div>
        <div class="post_sum">Posts:{{ head.post_sum }}</div>
      </div>
      <div class="container clearfix" v-for="item in topics" :key="item.topic_num">
        <manage :power="item.power" :board_num="board_num" :topic_num="item.topic_num"></manage>
        <div class="icon">
          <font-awesome-icon :icon="['fas', 'comment']" />
          <div class="post_sum">{{ item.post_sum - 1 }}</div>
        </div>
        <div class="left_container">
          <router-link :to="topic_url(item.topic_num)" class="topic" :title="item.topic" tag="div">
            {{ item.topic }}
          </router-link>
          <div class="date">{{ time_format(item.date) }}</div>
          <div class="creator">{{ item.creator }}</div>
        </div>
        <div class="right_container">
          <div class="last_post">
            <div class="last_poster">{{ item.poster }}</div>
            <div class="last_date">{{ time_format(item.last_date) }}</div>
          </div>
          <div class="button" @click="del(item.topic_num)" v-if="is_creator(item.creator)">
            <font-awesome-icon :icon="['fas', 'trash-alt']" />
          </div>
        </div>
      </div>
    </div>
    <page class="page_container" :current_page="page" :max_page="max_page" @page_turn="page_turn"></page>
    <post class="post_container" is_topic="true" :board_num="board_num"></post>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:8000/';
axios.defaults.withCredentials = true;

function get_data(to, from, next, vm_exist) {
  let path = to.path.split('/');
  let [board_num, page] = path[path.length - 1].split('-');

  // eslint-disable-next-line prettier/prettier
  if (
    /^[1-9][0-9]*$/.test(board_num) && 
    (page == undefined || /^[1-9][0-9]*$/.test(page))
  ) {
    page = page || 1;
    let vm;
    let get_vm = v => (vm = v);

    axios
      .get('/forum/' + board_num, {
        params: {
          page: page
        }
      })
      .then(response => {
        vm = vm || vm_exist;
        set_data(response, vm, page, board_num);
      });

    next(vm => {
      get_vm(vm);
    });
  } else {
    next('/404');
  }
}

function set_data(response, vm, page, board_num) {
  let topics = response.data.board_data;
  let head = response.data.board_information;

  for (let i = 0; i < topics.length; i++) {
    if (!topics[i]['power']) topics[i]['power'] = 0;
  }

  vm.board_num = board_num || vm.board_num;
  vm.page = Number(page) || vm.page;
  let max = head.topic_sum;
  max = Math.ceil(max / 20);
  max = max ? max : 1;
  vm.max_page = max;
  vm.$set(vm, 'topics', topics);
  vm.$set(vm, 'head', head);
}

export default {
  name: 'Board',
  data() {
    return {
      head: '',
      topics: '',
      board_num: '',
      page: 1,
      max_page: 1
    };
  },
  components: {
    manage: () => import('@/components/Manage'),
    post: () => import('@/components/Post'),
    page: () => import('@/components/Page')
  },
  methods: {
    topic_url(topic_num) {
      return '/forum/' + this.board_num + '/' + topic_num;
    },
    is_creator(creator) {
      return creator == this.$store.state.username;
    },
    del(topic_num) {
      if (this.$store.state.btn_switch) {
        this.$store.dispatch('btn_sleep');
        let page = this.page;
        if (this.topics.length == 1 && this.page != 1) {
          page = this.page - 1;
        }
        this.$axios
          .post('/forum/deletetopic', {
            board_num: this.board_num,
            topic_num: topic_num,
            page: this.page
          })
          .then(response => {
            if (response.status == 200) {
              set_data(response, this, page);
            }
          });
      }
    },
    page_turn(page) {
      let path = '/forum/' + this.board_num + '-' + page;
      this.$router.push({ path: path });
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
#board {
  .board_container {
    box-shadow: 0px 0px 5px rgb(80, 80, 80);
    margin-bottom: 5px;
    .head {
      border-bottom: 2px solid #ddd;
      background: rgb(75, 75, 75);
      .head_name {
        color: white;
        font-size: 1.875rem;
        margin: 3px 5px;
      }
      .topic_sum,
      .post_sum {
        display: inline-block;
        color: rgb(167, 167, 167);
        font-size: 0.875rem;
        margin: 3px 5px;
      }
    }
    .container {
      display: grid;
      grid-template-columns: 3.125rem 1fr 1fr;
      border-bottom: 2px solid rgb(206, 206, 206);
      background: rgba(245, 245, 245);
      transition: background 0.3s;
      .icon {
        width: 2.5rem;
        height: 2.5rem;
        color: rgb(102, 102, 102);
        font-size: 2.5rem;
        text-align: center;
        line-height: 1.875rem;
        margin: 5px;
        position: relative;
        .post_sum {
          display: flex;
          width: 0px;
          height: 0px;
          color: rgb(255, 255, 255);
          font-size: 0.625rem;
          line-height: 0.625rem;
          position: absolute;
          top: 50%;
          left: 50%;
          white-space: nowrap;
          justify-content: center;
          align-items: center;
        }
      }
      .left_container {
        display: grid;
        grid-template-columns: 6.25rem 1fr;
        padding: 5px;
        .topic {
          grid-column: ~'1 / 3';
          width: 13.75rem;
          color: rgb(81, 101, 214);
          font-size: 1rem;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
        }
        .topic:hover {
          text-decoration: underline;
        }
        .creator,
        .date {
          display: inline-block;
          color: #666;
          font-size: 0.875rem;
        }
      }
      .right_container {
        display: grid;
        grid-template-columns: 1fr 20px;
        align-content: center;
        text-align: right;
        color: #666;
        > div {
          font-size: 0.875rem;
        }
        .button {
          display: flex;
          justify-content: center;
          align-items: center;
          cursor: pointer;
        }
      }
    }
    .container:nth-child(2n + 1) {
      background: rgba(230, 230, 230);
    }
    .container:hover {
      background: rgb(202, 202, 202);
    }
  }
}
.clearfix::after {
  content: '';
  display: block;
  clear: both;
  height: 0;
  width: 0;
  visibility: hidden;
}
</style>
