<template>
  <div id="forum">
    <div class="forum_container">
      <div class="container" v-for="container in forum" :key="container.board_num">
        <div class="container_name">{{ container.name }}</div>
        <div class="board clearfix" v-for="item in container.boards" :key="item.board_num">
          <div class="icon">
            <font-awesome-icon :icon="['fas', 'comments']" />
          </div>
          <div class="left_container">
            <router-link :to="item.board_url || ''" class="board_name" tag="div">{{ item.name }}</router-link>
            <div class="topic_sum">Topics: {{ item.topic_sum }}</div>
            <div class="post_sum">Posts: {{ item.post_sum }}</div>
          </div>
          <div class="right_container">
            <router-link :to="item.post_url || ''" class="last_topic" tag="div">{{ item.last_topic }}</router-link>
            <div class="last_date">{{ time_format(item.last_date) }}</div>
            <div class="last_poster">{{ item.last_poster }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Forum',
  data() {
    return {
      forum: []
    };
  },
  created() {
    this.$axios.get('/forum/forumdata').then(response => {
      if (response.status == 200) {
        let forum_data = response.data.forum_data;
        forum_data.sort((a, b) => {
          return a['board_num'] - b['board_num'];
        });
        let forum = [];
        for (let data of forum_data) {
          if (data['board_num'] % 100 == 0) {
            data['boards'] = [];
            delete data['board_num'];
            forum.push(data);
          } else {
            let index = (data['board_num'] - (data['board_num'] % 100)) / 100 - 1;
            data['board_url'] = '/forum/' + data['board_num'];
            data['post_url'] = data['board_url'] + '/' + data['last_topic_num'];
            forum[index]['boards'].push(data);
          }
        }
        this.forum = forum;
      }
    });
  }
};
</script>

<style lang="less" scoped>
.forum_container {
  box-shadow: 0px 0px 5px rgb(80, 80, 80);
  .container {
    .container_name {
      text-align: left;
      font-size: 30px;
      color: white;
      background: rgb(75, 75, 75);
      padding: 3px 10px;
    }
    .board {
      border-bottom: 2px solid #ddd;
      background: #fff;
      .icon {
        float: left;
        width: 50px;
        height: 50px;
        color: rgb(75, 75, 75);
        font-size: 30px;
        text-align: center;
        line-height: 50px;
        margin: 10px;
      }
      .left_container {
        float: left;
        .board_name {
          margin: 5px;
          font-size: 22px;
          cursor: pointer;
        }
        .topic_sum,
        .post_sum {
          display: inline-block;
          color: #666;
          font-size: 14px;
          margin: 3px;
        }
      }
      .right_container {
        float: right;
        color: #666;
        font-size: 14px;
        padding: 10px;
        .last_topic {
          margin-bottom: 3px;
          cursor: pointer;
        }
        .last_topic:hover {
          text-decoration: underline;
        }
        .last_date,
        .last_poster {
          display: inline-block;
          margin-right: 10px;
        }
      }
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
