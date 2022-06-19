<template>
  <div class="search-box">
    <fa @click="openSearch()" icon="fa-solid fa-search" class="fa-search" />
    <div v-if="opened" class="search_container" id="search">
      <div class="search_line">
        <input
          v-show="!open_menu"
          type="text"
          class="input-search big_search"
          v-model="params.title"
          @keyup.enter="submit()"
        />
        <ul class="submenu">
          <li
            v-for="article in article_search"
            :key="article.id"
            @click="submitEasy(article.id)"
          >
            <p>{{ article.title }}</p>
          </li>
        </ul>
        <fa v-show="!open_menu" @click="submit" icon="fa-solid fa-search" />
        <fa @click="closeSearch()" icon="fa-solid fa-times" class="closeBtn" />
      </div>
      <button class="open_menu button" @click="open_menu = !open_menu">
        Расширенный поиск
      </button>
      <div v-show="open_menu" class="full_search">
        <h3>По названию</h3>
        <input
          type="text"
          class="input-search big_search"
          placeholder="Название"
          v-model="params.title"
        />
        <h3>По рейтингу</h3>
        <div>
          <input
            type="number"
            class="input-search"
            placeholder="Минимальный рейтинг"
            v-model="params.min_rating"
          />
          <input
            type="number"
            class="input-search"
            placeholder="Максимальный рейтинг"
            v-model="params.max_rating"
          />
        </div>
        <h3>По тегам</h3>
        <h4>Обязательно включать:</h4>
        <div class="tags">
          <ArticleTag
            :tags="tags_add"
            mode="search"
            :key="tags_and_key"
            @add="addAndTag"
            @remove="removeAndTag"
          />
        </div>
        <h4>Не включать:</h4>
        <div class="tags">
          <ArticleTag
            :tags="tags_del"
            :enable="true"
            :edit="true"
            mode="search"
            :key="tags_no_key"
            @add="addNoTag"
            @remove="removeNoTag"
          />
        </div>
        <h3>По авторам</h3>
        <h4>Обязательно включать:</h4>
        <div class="tags">
          <SearchUser
            :users="authorship_add"
            :key="users_and_key"
            @add="addAndUser"
            @remove="removeAndUser"
          />
        </div>
        <h4>Не включать:</h4>
        <div class="tags">
          <SearchUser
            :users="authorship_del"
            :key="users_no_key"
            @add="addNoUser"
            @remove="removeNoUser"
          />
        </div>
        <button class="open_menu button" @click="submit()">Искать!</button>
      </div>
    </div>
  </div>
</template>

<script>
import ArticleTag from "@/components/ArticleTag.vue";
import SearchUser from "@/components/SearchUser.vue";

export default {
  name: "SearchComponent",
  components: {
    ArticleTag,
    SearchUser,
  },
  computed: {
    article_search() {
      return this.$store.state.articles.article_search;
    },
  },
  methods: {
    addAndTag(tag) {
      this.tags_add.push(tag);
      this.params.tags_add.push(tag.id);
      this.tags_and_key += 1;
    },
    removeAndTag(tag) {
      this.tags_add.splice(this.tegs_add.indexOf(tag), 1);
      this.params.tags_add.splice(this.params.tags_add.indexOf(tag.id), 1);
      this.tags_and_key += 1;
    },
    addNoTag(tag) {
      this.tags_del.push(tag);
      this.params.tags_del.push(tag.id);
      this.tags_no_key += 1;
    },
    removeNoTag(tag) {
      this.tags_del.splice(this.tegs_del.indexOf(tag), 1);
      this.params.tags_del.splice(this.params.tags_del.indexOf(tag.id), 1);
      this.tags_no_key += 1;
    },
    addAndUser(user) {
      this.authorship_add.push(user);
      this.params.authorship_add.push(user.id);
      this.users_and_key += 1;
    },
    removeAndUser(user) {
      this.authorship_add.splice(this.authorship_add.indexOf(user), 1);
      this.params.authorship_add.splice(
        this.params.authorship_add.indexOf(user.id),
        1
      );
      this.users_and_key += 1;
    },
    addNoUser(user) {
      this.authorship_del.push(user);
      this.params.authorship_del.push(user.id);
      this.users_no_key += 1;
    },
    removeNoUser(user) {
      this.authorship_del.splice(this.authorship_del.indexOf(user), 1);
      this.params.authorship_del.splice(
        this.params.authorship_del.indexOf(user.id),
        1
      );
      this.users_no_key += 1;
    },
    closeSearch() {
      document.body.style.overflow = "scroll";
      this.open_menu = false;
      this.opened = false;
    },
    openSearch() {
      document.body.style.overflow = "hidden";
      this.opened = true;
    },
    submit() {
      this.closeSearch();
      this.$router.push({ path: "/search/article", query: this.params });
    },
    submitEasy(article_id) {
      this.closeSearch();
      this.$router.push(`/article/${article_id}`);
    },
  },
  data() {
    return {
      tags_no_key: 0,
      tags_and_key: 0,
      users_no_key: 0,
      users_and_key: 0,
      tags_add: [],
      tags_del: [],
      authorship_add: [],
      authorship_del: [],
      title: "",
      opened: false,
      open_menu: false,
      params: {
        title: "",
        min_rating: 0,
        max_rating: 0,
        tags_add: [],
        tags_del: [],
        authorship_add: [],
        authorship_del: [],
      },
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/search.scss"></style>
