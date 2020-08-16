<template>
  <div id="textedit" class="text" contenteditable="true" v-html="content" @input="input($event.target.innerHTML)"></div>
</template>

<script>
export default {
  name: 'TextEdit',
  props: ['text_first'],
  data() {
    return {
      text: '',
      content: ''
    };
  },
  methods: {
    input(text) {
      this.text = text;
      this.$emit('change_text', this.text);
    }
  },
  created() {
    this.content = this.text_first;
  }
};
</script>
