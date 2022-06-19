<template>
  <div>
    <FullHeader color="#0033ff" header="Scipher" />
    <div class="home">
      <h3>Найденные статьи</h3>
      <ShortenedArticle
        v-for="article in article_search"
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

export default {
  name: "SearchView",
  components: {
    FullHeader,
    ShortenedArticle,
  },
  computed: {
    article_search() {
      return this.$store.state.articles.article_search;
    },
  },
  beforeCreate() {
    const data = this.$route.query;
    if (typeof data.tags_add == "string")
      data.tags_add = data.tags_add ? [data.tags_add] : [];
    if (typeof data.tags_del == "string")
      data.tags_del = data.tags_del ? [data.tags_del] : [];
    if (typeof data.authorship_add == "string")
      data.authorship_add = data.authorship_add ? [data.authorship_add] : [];
    if (typeof data.authorship_del == "string")
      data.authorship_del = data.authorship_del ? [data.authorship_del] : [];
    this.$store.dispatch("SEARCH_ARTICLE", data);
  },
};
</script>

<style scoped lang="scss" src="../assets/scss/search_view.scss"></style>
