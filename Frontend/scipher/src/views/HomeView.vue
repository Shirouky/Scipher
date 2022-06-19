<template>
  <div>
    <FullHeader color="#0033ff" header="Scipher" />
    <Loader v-if="load" />
    <div class="home">
      <div class="left">
        <h3>Теги</h3>

        <div class="tags">
          <div
            v-for="tag in tags"
            :key="tag.id"
            class="tag"
            :style="{ 'background-color': tag.background_color }"
            @click="$router.push(`/tag/${tag.id}`)"
          >
            <p :style="{ color: tag.text_color }">{{ tag.title }}</p>
            <fa icon="fa-solid fa-arrow-right" />
          </div>
        </div>

        <h3>Лучшие статьи</h3>

        <ShortenedArticle
          v-for="article in popular_articles"
          :key="article.id"
          :article="article"
        />
      </div>
      <div class="right">
        <div class="rating_container">
          <h3>Пользователи</h3>

          <ShortenedUser v-for="user in users" :key="user.id" :user="user" />
        </div>
        <div class="rating_container">
          <h3>Последние статьи</h3>

          <ShortenedArticle
            v-for="article in latest_articles"
            :key="article.id"
            :article="article"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import FullHeader from "@/components/FullHeader.vue";
import ShortenedArticle from "../components/ShortenedArticle.vue";
import ShortenedUser from "../components/ShortenedUser.vue";
import Loader from "../components/Loader.vue";

export default {
  name: "HomeView",
  components: {
    FullHeader,
    ShortenedArticle,
    ShortenedUser,
    Loader,
  },
  computed: {
    tags_load() {
      return this.$store.state.tags.popular_tags_load;
    },
    popular_articles_load() {
      return this.$store.state.articles.popular_articles_load;
    },
    latest_articles_load() {
      return this.$store.state.articles.latest_articles_load;
    },
    users_load() {
      return this.$store.state.users.best_users_load;
    },
    load() {
      if (
        ((this.users_load == this.latest_articles_load) ==
          this.popular_articles_load) ==
        this.tags_load
      ) {
        document.body.style.overflow = "scroll";
        return true;
      } else return false;
    },
    tags() {
      return this.$store.state.tags.popular_tags;
    },
    popular_articles() {
      return this.$store.state.articles.popular_articles;
    },
    latest_articles() {
      return this.$store.state.articles.latest_articles;
    },
    users() {
      return this.$store.state.users.best_users;
    },
  },
  created() {
    this.$store.dispatch("SET_POPULAR_ARTICLES");
    this.$store.dispatch("SET_LATEST_ARTICLES");
    this.$store.dispatch("SET_POPULAR_TAGS");
    this.$store.dispatch("SET_BEST_USERS");
  },
};
</script>

<style scoped  lang="scss">
@import "../assets/scss/home.scss";
</style>
