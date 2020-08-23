<template>
  <div id="forum">
    <div class="forum_container">
      <div class="container" v-for="container in forum" :key="container.board_num">
        <manage power="1000" :board_num="container.board_num"></manage>
        <div class="container_name">{{ container.name }}</div>
        <div class="board clearfix" v-for="item in container.boards" :key="item.board_num">
          <manage power="1000" :board_num="item.board_num"></manage>
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
            <div class="last_poster">{{ item.last_poster }}</div>
            <div class="last_date">{{ time_format(item.last_date) }}</div>
          </div>
        </div>
      </div>
      <manage power="1000" :add_board="true"></manage>
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
  components: {
    manage: () => import('@/components/Manage.vue')
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
      font-size: 1.875rem;
      color: white;
      background: rgb(75, 75, 75);
      padding: 3px 10px;
    }
    .board {
      display: grid;
      grid-template-columns: 4.375rem 1fr 1fr;
      border-bottom: 2px solid #ddd;
      background: #fff;
      .icon {
        width: 3.125rem;
        height: 3.125rem;
        color: rgb(75, 75, 75);
        font-size: 1.875rem;
        text-align: center;
        line-height: 3.125rem;
        margin: 10px;
      }
      .left_container {
        .board_name {
          margin: 5px;
          font-size: 1.375rem;
          cursor: pointer;
        }
        .topic_sum,
        .post_sum {
          display: inline-block;
          color: #666;
          font-size: 0.875rem;
          margin: 3px;
        }
      }
      .right_container {
        display: grid;
        grid-template-columns: 1fr 7.5rem;
        grid-row-gap: 5px;
        grid-column-gap: 5px;
        align-content: center;
        text-align: right;
        color: #666;
        padding: 5px;
        .last_topic {
          grid-column: ~'1 / 3';
          font-size: 0.875rem;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
        }
        .last_topic:hover {
          text-decoration: underline;
        }
        .last_date,
        .last_poster {
          font-size: 0.875rem;
          line-height: 100%;
        }
        .last_poster {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          vertical-align: middle;
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
