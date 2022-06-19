

<template>
  <div>
    <ShortenedHeader />
    <div class="head">
      <div class="big_container">
        <div
          class="background"
          :style="{
            backgroundImage: `url(data:image/jpeg;base64,${
              user.background_img ? user.background_img : ''
            })`,
            backgroundColor: user.background_color,
            color: user.text_color,
          }"
        >
          <div class="upper">
            <div class="left_side">
              <span @click="$router.push(`/user/${user_id}`)" class="header">
                <div class="authors">
                  <img
                    class="avatar"
                    :src="`data:image/jpeg;base64,${
                      user.avatar ? user.avatar : ''
                    }`"
                  />
                </div>
                <h5 class="title">
                  {{ user.username }}
                </h5>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <figure class="tabBlock">
      <ul class="tabBlock-tabs">
        <li :aria-setsize="tabs.length" :aria-posinet="1">
          <a
            href="#home"
            class="tabBlock-tab"
            :class="active_tab === 0 ? 'is-active' : ''"
            :aria-selected="active_tab === 0"
            @click="changeTab(0)"
          >
            <fa style="margin-right: 10px" icon="fa fa-home"></fa>
            <strong>Главная</strong>
          </a>
        </li>
        <div v-if="show">
          <li
            v-for="(tab, index) in tabs"
            :key="index + 1"
            :aria-setsize="tabs.length + 1"
            :aria-posinet="index + 1"
          >
            <a
              :href="'#' + tab.href"
              class="tabBlock-tab"
              :class="active_tab === index + 1 ? 'is-active' : ''"
              :aria-selected="active_tab === index + 1"
              @click="changeTab(index + 1)"
            >
              <fa style="margin-right: 10px" :icon="tab.tab_icon"></fa>
              <strong>{{ tab.tab_title }}</strong>
            </a>
          </li>
        </div>
      </ul>
      <div class="tabBlock-content">
        <div
          name="home"
          :aria-current="active_tab === 0"
          class="tabBlock-pane"
          v-show="active_tab === 0"
        >
          <div class="home">
            <div class="left">
              <h3>Описание</h3>
              <div class="description" v-html="user.description"></div>
              <div class="button create" @click="openArticle()" v-if="show">
                <p>Создать статью</p>
                <fa icon="fa-solid fa-plus" />
              </div>
              <ul v-if="create_article_open" class="overlay_popup">
                <li class="header">
                  <b>Создать статью</b>
                  <fa
                    icon="fa-solid fa-times"
                    class="times fa-lg"
                    @click="create_article_open = false"
                  />
                </li>
                <li class="header">
                  <input
                    type="text"
                    placeholder="Название"
                    v-model="article_title"
                  />
                </li>
                <li class="header">
                  <button class="button green" @click="createArticle()">
                    Создать
                  </button>
                </li>
              </ul>
              <h3 v-if="user.authorship">Статьи пользователя</h3>
              <label for="slct" class="select" v-if="show">
                <select id="slct" required="required" v-model="user_option">
                  <option selected value="all">Все</option>
                  <option value="published" v-if="show">Готово</option>
                  <option value="in_work" v-if="show">В работе</option>
                </select>
              </label>
              <div v-else></div>
              <div v-if="user_option == 'all'">
                <ShortenedArticle
                  v-for="article in authorship_all"
                  :key="article.id"
                  :article="article"
                />
              </div>
              <div v-if="user_option == 'published'">
                <ShortenedArticle
                  v-for="article in authorship_published"
                  :key="article.id"
                  :article="article"
                />
              </div>
              <div v-if="user_option == 'in_work'">
                <ShortenedArticle
                  v-for="article in authorship_in_work"
                  :key="article.id"
                  :article="article"
                />
              </div>
            </div>
            <div class="right">
              <h3>Информация о пользователе</h3>
              <div class="info">
                <ul>
                  <li>
                    <p>День рождения:</p>
                    <span>{{
                      user.date_of_birth
                        ? user.date_of_birth.substring(0, 10)
                        : "Не указано"
                    }}</span>
                  </li>
                  <li>
                    <p>Последняя активность:</p>
                    <span>{{
                      user.last_activity
                        ? user.last_activity.substring(0, 10)
                        : "Не указано"
                    }}</span>
                  </li>
                  <li>
                    <p>Настоящее имя:</p>
                    <span>{{ user.first_name }} {{ user.second_name }}</span>
                  </li>
                  <li>
                    <p>Email:</p>
                    <span>{{ user.email }}</span>
                  </li>
                  <li>
                    <p>На сайте с:</p>
                    <span>{{
                      user.date_added
                        ? user.date_added.substring(0, 10)
                        : "Не указано"
                    }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div
          :aria-current="active_tab === 1"
          class="tabBlock-pane"
          v-show="active_tab === 1"
          name="articles"
        >
          <div class="home">
            <div class="button create" @click="openComp()">
              <p>Создать сборник</p>
              <fa icon="fa-solid fa-plus" />
            </div>
            <ul v-if="create_comp_open" class="overlay_popup">
              <li class="header">
                <b>Создать сборник</b>
                <fa
                  icon="fa-solid fa-times"
                  class="times fa-lg"
                  @click="create_comp_open = false"
                />
              </li>
              <li class="header">
                <input
                  type="text"
                  placeholder="Название"
                  v-model="comp_title"
                />
              </li>
              <li class="header">
                <button class="button green" @click="createComp()">
                  Создать
                </button>
              </li>
            </ul>
          </div>
          <figure class="tabBlock">
            <ul class="tabBlock-tabs">
              <li :aria-setsize="article_tabs.length" :aria-posinet="index + 1">
                <a
                  class="tabBlock-tab"
                  :class="active_article_tab === 0 ? 'is-active' : ''"
                  :aria-selected="active_article_tab === 0"
                  @click="changeArticleTab(0)"
                >
                  <strong>{{ article_tabs[0] }}</strong>
                </a>
                <a
                  class="tabBlock-tab"
                  :class="active_article_tab === 1 ? 'is-active' : ''"
                  :aria-selected="active_article_tab === 1"
                  @click="changeArticleTab(1)"
                >
                  <strong>{{ article_tabs[1] }}</strong>
                </a>
                <label
                  for="slct"
                  class="tabBlock-tab select"
                  :class="active_article_tab === 2 ? 'is-active' : ''"
                  :aria-selected="active_article_tab === 2"
                  @click="changeArticleTab(2)"
                >
                  <select id="slct" required="required" v-model="option">
                    <option value="" disabled="disabled" selected="selected">
                      Select option
                    </option>
                    <option
                      v-for="(compilation, index) in compilations"
                      :key="compilation.id"
                      :value="index"
                    >
                      {{ compilation.title }}
                    </option>
                  </select>
                </label>
              </li>
            </ul>
            <div class="tabBlock-content">
              <div
                name="read"
                :aria-current="active_article_tab === 0"
                class="tabBlock-pane"
                v-show="active_article_tab === 0"
              >
                <div class="home">
                  <ShortenedArticle
                    v-for="article in read"
                    :key="article.id"
                    :article="article"
                  />
                </div>
              </div>
            </div>
            <div class="tabBlock-content">
              <div
                name="viewed"
                :aria-current="active_article_tab === 1"
                class="tabBlock-pane"
                v-show="active_article_tab === 1"
              >
                <div class="home">
                  <ShortenedArticle
                    v-for="article in viewed"
                    :key="article.id"
                    :article="article"
                  />
                </div>
              </div>
            </div>
            <div class="tabBlock-content">
              <div
                name="personal"
                :aria-current="active_article_tab === 2"
                class="tabBlock-pane"
                v-show="active_article_tab === 2"
              >
                <div class="home">
                  <ShortenedArticle
                    v-for="article in compilations[option].articles"
                    :key="article.id"
                    :article="article"
                  />
                </div>
              </div>
            </div>
          </figure>
        </div>
        <div
          :aria-current="active_tab === 2"
          class="tabBlock-pane"
          v-show="active_tab === 2"
          name="comments"
        >
          <div class="home">
            <Comment
              v-for="comment in comments"
              :key="comment.id"
              :comment="comment"
              :show="false"
            />
          </div>
        </div>
        <div
          :aria-current="active_tab === 3"
          class="tabBlock-pane"
          v-show="active_tab === 3"
          name="settings"
        >
          <div class="home">
            <div class="settings">
              <h3 @click="$router.push(`/user/edit/${user_id}`)">
                Редактировать профиль
                <fa icon="fa-solid fa-pen-to-square" />
              </h3>
              <!-- <hr />
              <h3>Изменение логина</h3>
              <input
                class="input_change"
                placeholder="Логин"
                type="text"
                v-model="login"
              />
              <button class="button green_button" @click="saveLogin()">
                Сохранить
              </button>
              <hr />
              <h3>Изменение пароля</h3>
              <input
                class="input_change"
                placeholder="Пароль"
                type="password"
                v-model="password"
              />
              <input
                class="input_change"
                placeholder="Новый пароль"
                type="password"
                v-model="new_password"
              />
              <input
                class="input_change"
                placeholder="Подтвердите пароль"
                type="password"
                v-model="confirm_password"
              />
              <button class="button green_button" @click="savePassword()">
                Сохранить
              </button>
              <hr />
              <h3>Изменение email</h3>
              <input
                class="input_change"
                placeholder="Email"
                type="text"
                v-model="email"
              />
              <button class="button green_button" @click="saveEmail()">
                Сохранить
              </button> -->
            </div>
          </div>
        </div>
      </div>
    </figure>
  </div>
</template>




<script>
import ShortenedHeader from "@/components/ShortenedHeader.vue";
import ShortenedArticle from "@/components/ShortenedArticle.vue";
import Comment from "@/components/Comment.vue";

export default {
  name: "UserProfileView",
  components: {
    ShortenedHeader,
    ShortenedArticle,
    Comment,
  },
  created() {
    this.$store.dispatch("ADD_USER", this.user_id);
    if (this.show) this.$store.dispatch("SET_USER_AUTHORSHIP", this.user_id);
    const values = {
      "": 0,
      "#home": 0,
      "#articles": 1,
      "#comments": 2,
      "#settings": 3,
    };
    this.changeTab(values[this.$route.hash]);
  },
  mounted() {},
  computed: {
    show() {
      return this.$store.state.user && this.$store.state.user.id == this.user_id;
    },
    compilations() {
      return this.$store.state.compilations.user_compilations;
    },
    comments() {
      return this.$store.state.comments.user_comments;
    },
    viewed() {
      return this.$store.state.articles.user_viewed;
    },
    read() {
      return this.$store.state.articles.user_read;
    },
    authorship_in_work() {
      return this.$store.state.articles.authorship_in_work;
    },
    authorship_all() {
      return this.$store.state.articles.authorship_all;
    },
    authorship_published() {
      return this.$store.state.articles.authorship_published;
    },
    user() {
      const user = this.$store.getters.USER(this.user_id);
      if (user) return user;
      else return {};
    },
    user_id() {
      return this.$route.params.id;
    },
  },
  methods: {
    saveLogin() {
      this.$store.dispatch("SAVE_LOGIN", this.login);
    },
    savePassword() {
      if (
        this.new_password == this.confirm_password &&
        this.password == this.user.password
      ) {
        this.$store.dispatch("SAVE_PASSWORD", this.new_password);
      } else {
        this.$store.dispatch("SET_MESSAGE", ["error", "Ошибка"]);
      }
    },
    saveEmail() {
      this.$store.dispatch("CHECK_EMAIL", this.email);
      if (this.check_email) this.$store.dispatch("SAVE_EMAIL", this.email);
      else
        this.$store.disaptch("SET_MESSAGE", [
          "error",
          "Пользователь с таким email уже существует",
        ]);
    },
    openArticle() {
      this.create_article_open = true;
      this.article_title = "";
    },
    createArticle() {
      if (this.article_title != "") {
        this.$store.dispatch("CREATE_ARTICLE", this.article_title);
        this.create_article_open = false;
      }
    },
    openComp() {
      this.create_comp_open = true;
      this.comp_title = "";
    },
    createComp() {
      if (this.comp_title != "") {
        this.$store.dispatch("CREATE_COMPILATION", this.comp_title);
        this.create_comp_open = false;
      }
    },
    changeTab(tabIndexValue) {
      if ((tabIndexValue != 0 && this.show) || tabIndexValue == 0) {
        this.active_tab = tabIndexValue;
      }
      if (this.active_tab == 1) {
        this.$store.dispatch("SET_USER_VIEWED");
        this.$store.dispatch("SET_USER_READ");
        this.$store.dispatch("SET_USER_COMPILATIONS");
      } else if (this.active_tab == 2) {
        this.$store.dispatch("SET_USER_COMMENTS");
      }
    },
    changeArticleTab(tabIndexValue) {
      this.active_article_tab = tabIndexValue;
    },
  },
  data() {
    return {
      login: "",
      password: "",
      new_password: "",
      confirm_password: "",
      email: "",
      create_article_open: false,
      article_title: "",
      create_comp_open: false,
      comp_title: "",
      user_option: "all",
      option: 0,
      index: 0,
      active_tab: 0,
      active_article_tab: 0,
      article_tabs: ["Прочитанные", "Просмотренные"],
      tabs: [
        {
          tab_title: "Сохраненные статьи",
          tab_icon: "fa fa-bookmark",
          href: "articles",
        },
        {
          tab_title: "Комментарии",
          tab_icon: "fa fa-comments",
          href: "comments",
        },
        {
          tab_title: "Настройки",
          tab_icon: "fa fa-cogs",
          href: "settings",
        },
      ],
    };
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/user_profile.scss";
@import "../assets/scss/shortened_article.scss";
</style>