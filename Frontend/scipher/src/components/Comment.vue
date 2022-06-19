<template>
  <div class="comment_container" :style="{ border: author_border }">
    <div class="left" v-if="!is_author">
      <div>
        <fa
          icon="fa-solid fa-caret-up fa"
          ref="like"
          v-if="show"
          @click="like()"
        />
        <p v-if="comment.likes < 0" class="red">{{ comment.likes }}</p>
        <p v-else class="green">{{ comment.likes }}</p>
        <!-- <fa
          icon="fa-solid fa-caret-down fa"
          ref="dislike"
          v-if="show"
          @click="dislike()"
        /> -->
      </div>
    </div>
    <div class="right">
      <div class="flex">
        <div class="header">
          <div class="authors">
            <img
              class="avatar"
              :src="`data:image/jpeg;base64,${
                comment.author.avatar ? comment.author.avatar : ''
              }`"
              @click="$router.push(`/user/${comment.author.id}`)"
            />
            <p
              class="author"
              @click="$router.push(`/user/${comment.author.id}`)"
            >
              {{ comment.author.username }}
            </p>
            <p>{{ comment.date_added.slice(0, 10) }}</p>
          </div>
        </div>
        <div
          class="article"
          v-if="comment.article"
          @click="$router.push(`/article/${comment.article.id}`)"
        >
          <a>
            {{ comment.article.title }}
          </a>
          <fa icon="fa-solid fa-share" class="share" />
        </div>
      </div>
      <div v-if="comment.likes < -20">
        <p v-if="!display" @click="display = true" class="hidden">
          Комментарий скрыт из-за низкого рейтинга. Показать?
        </p>
        <p v-else>{{ comment.text }}</p>
      </div>
      <p v-else>{{ comment.text }}</p>

      <fa
        v-if="!is_author && show"
        icon="fa-solid fa-share"
        class="share"
        @click="openComment()"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseComment",
  props: {
    show: Boolean,
    comment: Object,
  },
  mounted() {
    if (this.is_author) this.$refs.like.classList.add(this.comment.is_liked ? "green" : "black");
    this.is_author = this.$cookies.get("id") == this.comment.author.id;
    this.author_border = this.is_author ? "solid 2px blue" : "$border";
  },
  methods: {
    openComment() {
      this.$emit("open", this.comment.id);
      document
        .getElementById("send_comment")
        .scrollIntoView({ behavior: "smooth" });
    },
    like() {
      // this.$refs.dislike.classList.remove("red");
      this.$emit("like");
      this.$refs.like.classList.toggle("green");
    },
    dislike() {
      this.$refs.like.classList.remove("green");
      // this.$refs.dislike.classList.add("red");
      this.$emit("dislike");
    },
  },
  data() {
    return {
      is_author: false,
      author_border: "",
      display: false,
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/comment.scss"></style>
