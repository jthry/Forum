<template>
  <div id="post">
    <div class="tip" v-if="is_topic">{{ topic_tip }}</div>
    <input type="text" class="topic" v-model="topic" v-if="is_topic" />
    <div class="tip">{{ post_tip }}</div>
    <textarea class="post" v-model="post"></textarea>
    <div class="tip">{{ submit_tip }}</div>
    <div class="submit" @click="submit">Post</div>
  </div>
</template>

<script>
export default {
  name: 'Post',
  props: ['is_topic', 'board_num', 'topic_num'],
  data() {
    return {
      topic: '',
      post: '',
      topic_tip: '',
      post_tip: '',
      submit_tip: ''
    };
  },
  watch: {
    topic() {
      if (this.is_topic) {
        if (this.topic) {
          let len = this.topic.length;
          if (len > 30) this.topic = this.topic.substring(0, 30);

          if (len > 20) this.topic_tip = 'Can also input ' + (30 - len) + ' words';
          else this.topic_tip = '';
        } else {
          this.topic_tip = '';
        }
      }
    },
    post() {
      if (this.post) {
        let len = this.post.length;
        if (len > 250) this.post = this.post.substring(0, 250);

        if (len > 230) this.post_tip = 'Can also input ' + (250 - len) + ' words';
        else this.post_tip = '';
      } else {
        this.post_tip = '';
      }
    }
  },
  methods: {
    submit() {
      if (this.$store.state.btn_switch) {
        if (this.is_topic) {
          if (this.topic != '' && this.post != '') {
            this.$store.dispatch('btn_sleep');
            this.$axios
              .post('/forum/addtopic', {
                board_num: this.board_num,
                topic: this.topic,
                post: this.post
              })
              .then(response => {
                if (response.status == 200) {
                  let path = '/forum/' + this.board_num + '/' + response.data.topic_num;
                  this.$router.push({ path });
                }
              })
              .catch(() => {
                alert('Post failed');
              });
          }
        } else {
          if (this.post != '') {
            this.$store.dispatch('btn_sleep');
            this.$axios
              .post('/forum/addpost', {
                board_num: this.board_num,
                topic_num: this.topic_num,
                post: this.post
              })
              .then(response => {
                if (response.data.code == 1) {
                  this.$router.go(0);
                }
              })
              .catch(() => {
                alert('Reply failed');
              });
          }
        }
      }
    }
  }
};
</script>

<style lang="less" scoped>
#post {
  padding: 20px 0;
  .tip {
    height: 18px;
    font-size: 14px;
    color: gray;
  }
  .topic {
    width: 100%;
    border: 1px solid white;
    box-shadow: 0px 0px 5px rgb(80, 80, 80);
    padding: 2px;
  }
  .post {
    width: 100%;
    height: 200px;
    border: 1px solid white;
    box-shadow: 0px 0px 5px rgb(80, 80, 80);
    padding: 2px;
    resize: none;
  }
  .submit {
    width: 50px;
    height: 30px;
    text-align: center;
    line-height: 30px;
    border: 1px solid rgb(196, 196, 196);
    background: white;
    box-shadow: 0px 0px 4px rgb(80, 80, 80);
    cursor: pointer;
  }
  .submit:hover {
    background: rgb(207, 207, 207);
  }
  .submit:active {
    background: rgb(182, 182, 182);
  }
}
</style>
