<template>
  <div>
    <ShortenedHeader />
    <Loader v-if="article_load" />
    <div class="head">
      <div
        class="buttons"
        @click="$router.push(article.id ? `/article/edit/${article.id}` : '')"
      >
        <div>
          <fa icon="fa-solid fa-arrow-right" />
          <a>Редактировать</a>
        </div>
      </div>
      <div
        class="big_container"
        :style="{
          backgroundColor: article.background_color,
          color: article.text_color,
        }"
      >
        <div
          class="background"
          :style="{
            backgroundImage: `url(data:image/jpeg;base64,${
              article.background_img ? article.background_img : ''
            })`,
          }"
        >
          <div class="upper">
            <div class="left_side">
              <span class="header">
                <div
                  v-for="author in article.authorship"
                  :key="author.id"
                  class="authors"
                  @click="$router.push(`/user/${author.id}`)"
                >
                  <img
                    class="avatar"
                    :src="`data:image/jpeg;base64,${
                      author.avatar ? author.avatar : ''
                    }`"
                  />
                  <p class="author">
                    {{ author.username }}
                  </p>
                </div>
                <p>
                  {{
                    article.date_added
                      ? article.date_added.substring(0, 10)
                      : ""
                  }}
                </p>
                <fa icon="fa-solid fa-eye" />
                <p class="views">{{ article.views }}</p>
              </span>
              <h5 class="title">
                {{ article.title }}
              </h5>
            </div>
            <div class="rating_container">
              <div class="rating">
                <p>{{ article.rating }}</p>
                <ul class="submenu">
                  <li>
                    <p>dasdads</p>
                  </li>
                  <li>
                    <button @click="userLogin()">Login</button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="description">
          <div class="tags_container">
            <div class="tags">
              <ArticleTag
                :tags="article.tags"
                mode="full_article"
                :edit="edit"
                :key="tagsKey"
                @add="addTag"
                @remove="removeTag"
              />
              <ArticleTag
                :tags="article.marks"
                mode="full_article"
                :edit="edit"
                :key="marksKey"
                @add="addMark"
                @remove="removeMark"
              />
            </div>
            <div class="period" v-if="article.period_start">
              <p>
                {{ article.period_start }}
                <br />
                <span v-if="article.period_end">
                  -
                  <br />
                  {{ article.period_end }}
                </span>
              </p>
            </div>
          </div>
          <div v-html="article.description"></div>
        </div>
      </div>
    </div>
    <div class="home">
      <div class="article" v-html="article.text"></div>

      <div class="save_buttons" v-if="show">
        <hr />
        <div
          class="read"
          :class="article.is_read ? 'green_button' : 'red_button'"
        >
          <input type="checkbox" v-model="article.is_read" />
          <label for="checkbox" @click="read()">{{
            article.is_read ? "Прочитано" : "Не прочитано"
          }}</label>
        </div>
        <button class="button" @click="getComps()">Сохранить в сборник</button>
        <ul v-if="open_compilation" class="overlay_popup">
          <Loader v-if="compilations_load" />
          <li class="header">
            <b>Сборники</b>
            <fa
              icon="fa-solid fa-times"
              class="times fa-lg"
              @click="open_compilation = false"
            />
          </li>
          <li
            @click="saveCompilation(comp)"
            v-for="comp in compilations"
            :key="comp.id"
            :class="comp.saved ? 'green_button' : 'red_button'"
          >
            {{ comp.title }}
          </li>
        </ul>
        <hr />
      </div>
      <Comment
        v-for="comment in article.comments"
        :key="comment.id"
        :comment="comment"
        :show="show"
        @like="likeComment(true, comment)"
        @dislike="likeComment(false, comment)"
        @open="openComment()"
      />
      <div class="send_comment" id="send_comment">
        <button
          v-if="!open_comment && show"
          @click="open_comment = true"
          class="button"
        >
          Оставить комментарий
        </button>
        <div class="comm" v-if="open_comment">
          <textarea v-model="comment" />
          <div class="icons">
            <fa
              icon="fa-solid fa-arrow-right"
              @click="sendComment()"
              class="fa-arrow-right fa-xl"
            />
            <fa
              icon="fa-solid fa-times"
              @click="open_comment = false"
              class="fa-times fa-xl"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ShortenedHeader from "@/components/ShortenedHeader.vue";
import Comment from "@/components/Comment.vue";
import Loader from "@/components/Loader.vue";
import ArticleTag from "@/components/ArticleTag.vue";

export default {
  name: "ArticleView",
  components: {
    ShortenedHeader,
    Comment,
    Loader,
    ArticleTag,
  },
  created() {
    this.$store.dispatch("ADD_VIEWED", this.article_id);
    this.$store.dispatch("ADD_ARTICLE", this.article_id);
  },
  computed: {
    show() {
      if (this.article.is_author || this.article.is_read || !this.is_auth)
        return false;
      else return true;
    },
    auth() {
      return this.$store.state.is_auth;
    },
    article_load() {
      return this.$store.state.articles.article_load;
    },
    article() {
      const article = this.$store.getters.ARTICLE(this.article_id);
      this.updateTags();
      if (article) return article;
      else return {};
    },
    compilations() {
      return this.$store.state.compilations.compilations;
    },
    compilations_load() {
      return this.$store.state.compilations.compilations_load;
    },
    article_id() {
      return this.$route.params.id;
    },
  },
  mounted() {
    // const that = this;
    // that.$store.dispatch("SET_READ", {
    //   user_id: that.user_id,
    //   article_id: that.article_id,
    // });
    // if (that.likes != {}) {
    //   that.$store.dispatch("SET_LIKES", that.likes);
    //   that.likes = {};
    // }
  },
  // beforeDestroy() {
  //   if (this.update_is_read != this.article.is_read) {
  //     this.$store.dispatch("SET_READ", {
  //       user_id: this.user_id,
  //       article_id: this.article_id,
  //     });
  //     this.article.is_read = this.update_is_read;
  //   }
  //   // if (this.likes) this.$store.dispatch("SET_LIKES", this.likes);
  // },
  methods: {
    read() {
      this.article.is_read = !this.article.is_read;
      this.$store.dispatch("SET_READ", this.article_id);
    },
    updateTags() {
      this.tagsKey += 1;
    },
    openComment(answer_id) {
      this.answer_id = answer_id;
      this.open_comment = true;
    },
    getComps() {
      this.open_compilation = true;
      this.$store.dispatch("SET_COMPILATIONS", this.article_id);
    },
    saveCompilation(compilation) {
      this.open_compilation = false;
      if (!compilation.saved) {
        const data = {
          article_id: this.article.id,
          compilation_id: compilation.id,
        };
        this.$store.dispatch("SAVE_COMPILATION", data);
        compilation.saved = true;
      }
    },
    likeComment(comm, comment) {
      if (comm) {
        if (comment.is_liked) {
          this.$set(comment, "likes", comment.likes - 1);
        } else {
          this.$set(comment, "likes", comment.likes + 1);
        }
      }
      this.$set(comment, "is_liked", !comment.is_liked);
      this.$store.dispatch("SET_LIKES", comment.id);
      // else {
      //   if (comment.user_like == "like") {
      //     this.$set(comment, "likes", comment.likes - 2);
      //     this.likes[comment.id] = "dislike";
      //   } else if (comment.user_like == "") {
      //     this.$set(comment, "likes", comment.likes - 1);
      //     this.likes[comment.id] = "dislike";
      //   } else {
      //     this.$set(comment, "likes", comment.likes + 1);
      //     this.likes[comment.id] = "none";
      //   }
      // }
    },
    removeTag(tag) {
      this.article.tags.splice(this.article.tags.indexOf(tag), 1);
      this.edit = true;
      this.updateTags();
    },
    addTag(tag) {
      this.article.tags.push(tag);
      this.edit = true;
      this.updateTags();
    },
    removeMark(mark) {
      this.article.marks.splice(this.article.marks.indexOf(mark), 1);
      this.edit = true;
      this.updateMarks();
    },
    addMark(mark) {
      this.article.marks.push(mark);
      this.edit = true;
      this.updateMarks();
    },
    sendComment() {
      const data = {
        origin_id: this.article_id,
        answer_id: this.answer_id,
        text: this.comment,
        type: "article",
      };
      this.$store.dispatch("SEND_COMMENT", data);
      this.open_comment = false;
    },
  },
  data() {
    return {
      likes: {},
      open_compilation: false,
      header_key: 0,
      comment: "",
      open_comment: false,
      answer_id: 0,
      edit: false,
      tagsKey: 0,
      marksKey: -1,
    };
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/article.scss";
@import "../assets/scss/shortened_article.scss";
</style>
