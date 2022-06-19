<template>
  <div
    class="container"
    :style="{
      backgroundColor: article.background_color,
      color: article.text_color,
      border: border,
    }"
  >
    <div
      :class="{
        is_read: article.is_read,
        is_author: article.is_author,
        background: true,
      }"
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
              v-for="author in article.authors"
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
              <p>
                {{ author.username }}
              </p>
            </div>
            <p>{{ article.date_added.slice(0, 10) }}</p>
            <fa icon="fa-solid fa-eye" class="fa-eye" />
            <p class="views">{{ article.views }}</p>
          </span>
          <h5 @click="$router.push(`/article/${article.id}`)" class="title">
            {{ article.title }}
          </h5>
        </div>
        <div class="rating_container">
          <div class="rating">
            <p>{{ article.rating }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="description">
      <div class="tags_container">
        <div class="tags">
          <ArticleTag
            :tags="article.tags"
            :edit="edit"
            mode="short_article"
            :key="tagsKey"
          />
          <ArticleTag
            :tags="article.marks"
            :edit="edit"
            mode="short_article"
            :key="marksKey"
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
      <p class="description_text" v-html="article.description"></p>
    </div>
  </div>
</template>

<script>
import ArticleTag from "@/components/ArticleTag.vue";

export default {
  name: "ShortenedArticle",
  props: {
    article: Object,
  },
  components: { ArticleTag },
  computed: {
    border() {
      return this.article.background_img
        ? ""
        : "1px solid #d2d9e1";
    },
  },
  data() {
    return {
      tagsKey: 0,
      marksKey: 1,
      enable: false,
      edit: false,
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/shortened_article.scss"></style>
