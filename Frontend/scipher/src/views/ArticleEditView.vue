<template>
  <div>
    <ShortenedHeader />
    <Loader v-if="article_load" />
    <div class="head buttons">
      <div @click="$router.push({ name: 'article' })">
        <fa icon="fa-solid fa-arrow-right" />
        <a>Публичная страница</a>
      </div>
      <div @click="deleteArticle()">
        <fa icon="fa-solid fa-trash" />
        Удалить статью
      </div>
    </div>
    <div class="buttons">
      <label for="font_color" class="button">Цвет текста </label>
      <label for="back_color" class="button">Цвет фона </label>
      <label for="back_img" class="button">Фоновое изображение </label>
      <button class="button" @click="publish()" v-if="!article.published">
        Опубликовать
      </button>
      <input
        type="color"
        id="font_color"
        class="input"
        v-model="article.text_color"
      />
      <input
        type="color"
        id="back_color"
        class="input"
        v-model="article.background_color"
      />
      <input
        class="input"
        type="file"
        accept="image/*"
        id="back_img"
        @change="backgroundImg"
      />
    </div>
    <div class="big_container">
      <div
        class="background"
        :style="{
          backgroundImage: background_img,
          backgroundColor: article.background_color,
          color: article.text_color,
        }"
        :key="keyBack"
      >
        <div class="upper">
          <div class="left_side">
            <span class="header">
              <div>
                <div class="authors">
                  <div
                    v-for="author in article.authorship"
                    :key="author.id"
                    class="authors"
                  >
                    <img
                      class="avatar"
                      :src="`data:image/jpeg;base64,${
                        author.avatar ? author.avatar : ''
                      }`"
                      @click="$router.push('/user/' + author.id)"
                    />
                    <p
                      @click="$router.push('/user/' + author.id)"
                      class="author"
                    >
                      {{ author.username }}
                    </p>
                  </div>
                  <fa
                    v-if="!edit_authors"
                    @click="edit_authors = true"
                    icon="fa-solid fa-pen-to-square"
                  />
                </div>
                <div class="input_container" v-if="edit_authors">
                  <input
                    @input="searchUser()"
                    type="text"
                    class="input-search"
                    placeholder="Укажите автора"
                    v-model="user_input"
                  />
                  <ul class="submenu">
                    <li
                      v-for="user in user_search"
                      :key="user.id"
                      @click="addUser(user)"
                    >
                      <p>{{ user.username }}</p>
                    </li>
                  </ul>
                  <fa
                    @click="edit_authors = false"
                    class="fa-xl"
                    icon="fa-solid fa-times"
                  />
                </div>
              </div>
            </span>
            <input
              :style="{
                color: article.text_color,
              }"
              class="label title"
              v-model="article.title"
            />
          </div>
        </div>
      </div>

      <div
        class="description"
        :style="{
          backgroundColor: article.background_color,
          color: article.text_color,
        }"
      >
        <div class="tags_container">
          <div class="tags">
            <ArticleTag
              :tags="article.tags"
              mode="edit_article"
              :key="tagsKey"
              @add="addTag"
              @remove="removeTag"
            />
          </div>
          <div class="period" v-if="article.period_start">
            <label for="period_start"
              >Начало периода:
              <input
                type="date"
                v-model="article.period_start"
                id="period_start"
            /></label>
            <br />
            -
            <br />
            <label for="period_end"
              >Конец периода:
              <input type="date" v-model="article.period_end" id="period_end"
            /></label>
          </div>
        </div>
        <ckeditor
          v-model="article.description"
        ></ckeditor>
      </div>
      <div class="home">
        <ckeditor v-model="article.text" :config="editor_config"></ckeditor>
      </div>
    </div>
  </div>
</template>

<script>
import ArticleTag from "@/components/ArticleTag.vue";
import ShortenedHeader from "@/components/ShortenedHeader.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "ArticleEditView",
  components: {
    ArticleTag,
    Loader,
    ShortenedHeader,
  },
  beforeDestroy() {
    clearInterval(this.timer)
    this.save();
  },
  mounted() {
    const that = this;
    this.$store.dispatch("ADD_ARTICLE", this.article_id);
    that.timer = setInterval(function tick() {
      that.$store.dispatch("SAVE_ARTICLE", {
        data: that.data,
        article_id: that.article_id,
      });
      if (
        typeof that.article.background_img != "string" &&
        that.article.background_img
      ) {
        that.$store.dispatch("SAVE_ARTICLE_BACK", {
          article_id: that.article.id,
          file: that.article.background_img,
        });
      }
    }, 5000);
  },
  computed: {
    data() {
      var tags = [];
      this.article.tags.forEach((tag) => {
        tags.push(tag.id);
      });
      return {
        title: this.article.title,
        description: this.article.description,
        text: this.article.text,
        background_color: this.article.background_color
          ? this.article.background_color
          : "#ffffff",
        text_color: this.article.text_color
          ? this.article.text_color
          : "#000000",
        is_published: this.article.published,
        tags: tags,
      };
    },
    article() {
      const article = this.$store.getters.ARTICLE(this.article_id);
      this.updateTags();
      if (article) return article;
      else return { tags: [] };
    },
    article_id() {
      return this.$route.params.id;
    },
    article_load() {
      return this.$store.state.articles.article_load;
    },
    user_search() {
      return this.$store.state.users.user_search;
    },
    editor_config() {
      return this.$store.state.editor_config;
    },
    background_img() {
      if (typeof this.article.background_img == "string") {
        return `url(data:image/jpeg;base64,${
          this.article.background_img ? this.article.background_img : ""
        })`;
      } else {
        var data = new Blob([this.article.background_img]);
        return "url(" + String(URL.createObjectURL(data)) + ")";
      }
    },
  },
  methods: {
    updateTags() {
      this.tagsKey += 1;
    },
    deleteArticle() {
      this.$store.dispatch("DELETE_ARTICLE", this.article.id);
      this.$router.push("/");
    },
    publish() {
      this.$store.dispatch("PUBLISH_ARTICLE", this.article.id);
    },
    addUser(user) {
      this.user_input = "";
      this.article.authorship.push(user);
    },
    searchUser() {
      this.$store.dispatch("SEARCH_USER", this.user_input);
    },
    backgroundImg(event) {
      this.article.background_img = event.target.files[0];
    },
    save() {
      this.$store.dispatch("SAVE_ARTICLE", this.article);
    },
    removeTag(tag) {
      this.article.tags.splice(this.article.tags.indexOf(tag), 1);
      this.tagsKey += 1;
    },
    addTag(tag) {
      this.article.tags.push(tag);
      this.tagsKey += 1;
    },
  },
  data() {
    return {
      edit_authors: false,
      user_input: "",
      keyBack: 1,
      display: "none",
      tagsKey: 1,
      timer: "",
    };
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/article_edit.scss";
@import "../assets/scss/shortened_article.scss";
</style>
