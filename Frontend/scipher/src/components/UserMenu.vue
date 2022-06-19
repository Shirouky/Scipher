<template>
  <div>
    <div class="container" v-if="user.id">
      <div class="avatar" @click="openNav()">
        <p>{{ user.username }}</p>
        <img
          :src="`data:image/jpeg;base64,${user.avatar ? user.avatar : ''}`"
        />
        <fa icon="fa-solid fa-caret-down" />
      </div>
      <div id="myNav" class="overlay closed">
        <fa @click="closeNav()" icon="fa-solid fa-times" class="closeBtn" />
        <div class="overlay-content">
          <div class="wrapper">
            <a @click="$router.push(`/user/${user.id}`)">Профиль</a>
          </div>
          <div class="wrapper">
            <a class="exit" @click="userLogout()">Выход</a>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="login_container">
      <strong class="login">Вход</strong>
      <ul class="submenu">
        <li>
          <p v-show="error_message">{{ error_message }}</p>
        </li>
        <li>
          <input
            v-model="email"
            type="email"
            aria-describedby="emailHelp"
            placeholder="Email"
          />
        </li>
        <li>
          <input v-model="password" type="password" placeholder="Password" />
        </li>
        <li>
          <button @click="userLogin()" class="green_button">Вход</button>
        </li>
      </ul>
      <a @click="$router.push('/register')">Регистрация</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserMenu",
  created() {
    this.getUserData();
  },
  computed: {
    user() {
      return this.$store.state.users.user;
    },
  },
  methods: {
    getUserData() {
      if (this.$cookies.get("token")) {
        this.$store.dispatch("SET_USER");
      }
    },
    userLogout() {
      this.$store.dispatch("LOGOUT_USER");
      this.$router.go();
    },
    userLogin() {
      if (this.login != "" && this.password != "") {
        this.$store.dispatch("LOGIN_USER", {
          username: this.email,
          password: this.password,
        });
      } else {
        this.error_message = "Даные введены не полностью";
      }

      if (typeof this.user != "object") {
        this.error_message = this.user;
      }
    },
    openNav() {
      const nav = document.getElementById("myNav");
      nav.classList.add("opened");
      nav.classList.remove("closed");
    },

    closeNav() {
      const nav = document.getElementById("myNav");
      nav.classList.add("closed");
      nav.classList.remove("opened");
    },
  },
  data() {
    return {
      email: "",
      password: "",
      error_message: "",
    };
  },
};
</script>


<style scoped lang="scss">
@import "../assets/scss/user_menu.scss";
</style>
