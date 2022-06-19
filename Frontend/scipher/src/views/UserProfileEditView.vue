<template>
  <div>
    <ShortenedHeader />
    <div class="buttons head">
      <label for="font_color" class="button">Цвет текста </label>
      <label for="back_color" class="button">Цвет фона </label>
      <label for="back_img" class="button">Фоновое изображение </label>
      <label for="avatar" class="button">Аватар </label>
      <input
        type="color"
        id="font_color"
        class="input"
        v-model="user.text_color"
      />
      <input
        type="color"
        id="back_color"
        class="input"
        v-model="user.background_color"
      />
      <input
        class="input"
        type="file"
        accept="image/*"
        id="back_img"
        @change="backgroundImg"
      />
      <input
        class="input"
        type="file"
        accept="image/*"
        id="avatar"
        @change="avatar"
      />
    </div>
    <div class="big_container">
      <div
        class="background"
        :style="{
          backgroundImage: background_img,
          backgroundColor: user.background_color,
          color: user.text_color,
        }"
      >
        <div class="upper">
          <div class="left_side">
            <span class="header">
              <div class="authors">
                <img class="avatar" :src="avatar_img" />
              </div>
              <input
                :style="{ color: user.text_color }"
                v-model="user.username"
                class="label title"
              />
            </span>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="home">
        <div class="left">
          <h3>Описание</h3>
          <div class="description">
            <ckeditor
              v-model="user.description"
              :config="editor_config"
            ></ckeditor>
          </div>
        </div>
        <div class="right">
          <h3>Информация о пользователе</h3>
          <div class="info">
            <ul>
              <li>
                <p>День рождения:</p>
                <input
                  type="date"
                  v-model="user.date_of_birth"
                  class="inputs"
                  id="period_start"
                />
              </li>
              <li>
                <p>Настоящее имя:</p>
                <span>
                  <input
                    placeholder="Имя"
                    class="inputs"
                    v-model="user.first_name"
                  />
                  <input
                    placeholder="Фамилия"
                    class="inputs"
                    v-model="user.second_name"
                  />
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>




<script>
import ShortenedHeader from "@/components/ShortenedHeader.vue";

export default {
  name: "UserProfileView",
  components: {
    ShortenedHeader,
  },
  created() {
    this.$store.dispatch("ADD_USER", this.uid);
  },
  beforeDestroy() {
    this.$store.dispatch("SAVE_USER", this.dat);
    clearInterval(this.tick)
  },
  mounted() {
    const that = this;
    this.tick = setInterval(function tick() {
      that.$store.dispatch("SAVE_USER", that.dat);
      if (typeof that.user.avatar != "string") {
        that.$store.dispatch("SAVE_AVATAR", that.user.avatar);
      }
      if (typeof that.user.background_img != "string") {
        that.$store.dispatch("SAVE_USER_BACK", that.user.background_img);
      }
    }, 5000);
  },
  computed: {
    editor_config() {
      return this.$store.state.editor_config;
    },
    user() {
      const user = this.$store.getters.USER(this.uid);
      if (user) return user;
      else return {};
    },
    uid() {
      return this.$route.params.id;
    },
    avatar_img() {
      if (typeof this.user.avatar == "string") {
        return `data:image/jpeg;base64,${
          this.user.avatar ? this.user.avatar : ""
        }`;
      } else {
        var data = new Blob([this.user.avatar]);
        return String(URL.createObjectURL(data));
      }
    },
    background_img() {
      if (typeof this.user.background_img == "string") {
        return `url(data:image/jpeg;base64,${
          this.user.background_img ? this.user.background_img : ""
        })`;
      } else {
        var data = new Blob([this.user.background_img]);
        return "url(" + String(URL.createObjectURL(data)) + ")";
      }
    },
    dat() {
      const data = {
        username: this.user.username,
        first_name: this.user.first_name,
        second_name: this.user.second_name,
        date_of_birth: this.user.date_of_birth,
        description: this.user.description,
        background_color: this.user.background_color
          ? this.user.background_color
          : "",
        text_color: this.user.text_color ? this.user.text_color : "#000000",
      };
      console.log(data);
      return data;
    },
  },
  methods: {
    avatar(event) {
      this.user.avatar = event.target.files[0];
    },
    backgroundImg(event) {
      this.user.background_img = event.target.files[0];
    },
  },
  data() {
    return {
      tick: "",
    };
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/user_profile.scss";
@import "../assets/scss/shortened_article.scss";
</style>
