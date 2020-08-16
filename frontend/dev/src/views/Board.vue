<template>
  <div id="board">
    <div class="board_container">
      <div class="head">
        <div class="head_name">{{ head.name }}</div>
        <div class="topic_sum">Topics:{{ head.topic_sum }}</div>
        <div class="post_sum">Posts:{{ head.post_sum }}</div>
      </div>
      <div class="container clearfix" v-for="item in topics" :key="item.topic_num">
        <div class="icon">
          <font-awesome-icon :icon="['fas', 'comment']" />
          <div class="post_sum">{{ item.post_sum - 1 }}</div>
        </div>
        <div class="left_container">
          <router-link :to="topic_url(item.topic_num)" class="topic" :title="item.topic" tag="div">
            {{ item.topic }}
          </router-link>
          <div class="creator">{{ item.creator }}</div>
          <div class="date">{{ time_format(item.date) }}</div>
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
        if (this.topics == 1 && this.page != 1) {
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
              let topics = response.data.board_data;
              let head = response.data.board_information;

              this.page = page;
              let max = head.topic_sum;
              max = max / 20 + (max % 20) ? 1 : 0;
              this.max_page = max;

              this.$set(this, 'topics', topics);
              this.$set(this, 'head', head);
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
    let path = to.path.split('/');
    let [board_num, page] = path[path.length - 1].split('-');

    // eslint-disable-next-line prettier/prettier
    if (
      /^[1-9][0-9]*$/.test(board_num) && 
      (page == undefined || /^[1-9][0-9]*$/.test(page))
    ) {
      page = Number(page) || 1;
      let vm;
      let getVm = v => (vm = v);

      axios
        .get('/forum/' + board_num, {
          params: {
            page: page
          }
        })
        .then(response => {
          let topics = response.data.board_data;
          let head = response.data.board_information;
          vm.board_num = board_num;

          vm.page = page;
          let max = head.topic_sum;
          max = Math.ceil(max / 20);
          vm.max_page = max;

          vm.$set(vm, 'topics', topics);
          vm.$set(vm, 'head', head);
        });

      next(vm => {
        getVm(vm);
      });
    } else {
      next('/404');
    }
  },
  beforeRouteUpdate(to, from, next) {
    let path = to.path.split('/');
    let [board_num, page] = path[path.length - 1].split('-');

    // eslint-disable-next-line prettier/prettier
    if (
      /^[1-9][0-9]*$/.test(board_num) &&
      (page == undefined || /^[1-9][0-9]*$/.test(page))
    ) {
      page = Number(page) || 1;
      axios
        .get('/forum/' + board_num, {
          params: {
            page: page
          }
        })
        .then(response => {
          let topics = response.data.board_data;
          let head = response.data.board_information;
          this.board_num = board_num;

          this.page = page;
          let max = head.topic_sum;
          max = Math.ceil(max / 20);
          this.max_page = max;

          this.$set(this, 'topics', topics);
          this.$set(this, 'head', head);
        });

      next();
    } else {
      next('/404');
    }
  }
};
</script>

<style lang="less" scoped>
#board {
  padding: 3%;
  .board_container {
    box-shadow: 0px 0px 5px rgb(80, 80, 80);
    margin-bottom: 5px;
    .head {
      border-bottom: 2px solid #ddd;
      background: rgb(75, 75, 75);
      .head_name {
        color: white;
        font-size: 30px;
        margin: 3px 5px;
      }
      .topic_sum,
      .post_sum {
        display: inline-block;
        color: rgb(167, 167, 167);
        font-size: 14px;
        margin: 3px 5px;
      }
    }
    .container {
      border-bottom: 2px solid rgb(206, 206, 206);
      background: rgba(245, 245, 245);
      transition: background 0.3s;
      .icon {
        float: left;
        color: rgb(102, 102, 102);
        font-size: 40px;
        text-align: center;
        line-height: 30px;
        margin: 5px;
        position: relative;
        .post_sum {
          display: flex;
          width: 0px;
          height: 0px;
          color: rgb(255, 255, 255);
          font-size: 10px;
          line-height: 10px;
          position: absolute;
          top: 50%;
          left: 50%;
          white-space: nowrap;
          justify-content: center;
          align-items: center;
        }
      }
      .left_container {
        float: left;
        padding: 5px;
        .topic {
          display: block;
          width: 220px;
          color: rgb(81, 101, 214);
          font-size: 16px;
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
          font-size: 14px;
          margin-right: 10px;
        }
      }
      .right_container {
        float: right;
        text-align: right;
        margin-top: 7px;
        color: #666;
        > div {
          display: inline-block;
          font-size: 14px;
          margin: 0 20px 0 0;
          vertical-align: middle;
        }
        .button {
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