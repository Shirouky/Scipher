<template>
  <div>
    <FullHeader />
    <Loader v-if="tag_load" />
    <div class="home">
      <div
        class="tag_container"
        :style="{
          backgroundColor: tag.category.background_color,
          color: tag.category.text_color,
        }"
      >
      <div>
        <h3>Тэг: {{ tag.title }}</h3>
        <p style="white-space: pre-line">{{ tag.description }}</p>
        </div>
        <div class="category_container">
          <h3 @click="$router.push(`/category/${tag.category ? tag.category.id : ''}`)">Категория: {{ tag.category ? tag.category.title : '' }}</h3>
          <p>{{ tag.category ? tag.category.description : ''}}</p>
        </div>
      </div>
      <h3>Статьи с данным тегом</h3>
      <ShortenedArticle
        v-for="article in tag_articles"
        :key="article.id"
        :article="article"
      />
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import FullHeader from "@/components/FullHeader.vue";
import ShortenedArticle from "@/components/ShortenedArticle.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "TagView",
  components: {
    FullHeader,
    ShortenedArticle,
    Loader,
  },
  created() {
    this.$store.dispatch("ADD_TAG", this.tag_id);
    this.$store.dispatch("SET_TAG_ARTICLES", this.tag_id);
  },
  computed: {
    tag_id() {
      return this.$route.params.id;
    },
    tag_load() {
      return this.$store.state.tags.tag_load;
    },
    tag() {
      const tag = this.$store.getters.TAG(this.tag_id);
      if (tag) return tag;
      else return {};
    },
    tag_articles() {
      return this.$store.state.articles.tag_articles;
    },
  },
  data() {
    return {
      params: [],
    };
  },
};
</script>

<style scoped lang="scss" src="../assets/scss/search_view.scss"></style>
