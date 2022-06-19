<template>
  <div>
    <FullHeader />
    <div class="big_head"></div>
    <figure class="tabBlock">
      <ul class="tabBlock-tabs">
        <li
          v-for="(tab, index) in tabs"
          :key="index"
          :aria-setsize="tabs.length"
          :aria-posinet="index"
          @click="changeTab(index)"
        >
          <a
            class="tabBlock-tab"
            :class="active_tab === index ? 'is-active' : ''"
            :aria-selected="active_tab === index"
            @click="changeTab(index)"
          >
            <fa style="margin-right: 10px" :icon="tab.tab_icon"></fa>
            <strong>{{ tab.tab_title }}</strong>
          </a>
        </li>
      </ul>
      <div class="tabBlock-content">
        <div
          :aria-current="active_tab === 0"
          class="tabBlock-pane"
          v-show="active_tab === 0"
        >
          <div class="home_">
            <div class="confirmation">
              <input
                type="text"
                v-model="email"
                id="email"
                placeholder="Email"
              />
              <div @click="sendConfiramtion()">
                Отправить подтверждение на почту
                <fa icon="fa-solid fa-arrow-right" />
              </div>
            </div>
            <input
              :class="checkEmail"
              type="number"
              v-model="confirm_email"
              placeholder="Подтвердите email"
              :disabled="!enable_email"
            />
            <div class="next_button" @click="firstStep()">
              <p>К следующему шагу</p>
              <fa icon="fa-solid fa-arrow-right" />
            </div>
          </div>
        </div>
        <div
          :aria-current="active_tab === 1"
          class="tabBlock-pane"
          v-show="active_tab === 1"
        >
          <div class="home_">
            <div class="confirmation important">
              <input
                type="text"
                v-model="login"
                placeholder="Логин"
                :class="login ? 'green' : 'red'"
              />
              <input
                type="text"
                v-model="username"
                placeholder="Имя пользователя"
                :class="username ? 'green' : 'red'"
              />
              <input
                type="password"
                v-model="password"
                placeholder="Пароль"
                :class="password ? 'green' : 'red'"
              />
              <input
                type="password"
                v-model="confirm_password"
                placeholder="Подтвердите пароль"
                :class="checkPassword"
                :disabled="password == ''"
              />
            </div>
            <div class="next_button" @click="secondStep()">
              <p>Завершить регистрацию</p>
              <fa icon="fa-solid fa-arrow-right" />
            </div>
          </div>
        </div>
      </div>
    </figure>
  </div>
</template>




<script>
import FullHeader from "@/components/FullHeader.vue";

export default {
  name: "RegisterView",
  components: {
    FullHeader,
  },
  computed: {
    checkEmail() {
      if (this.confirm_email == this.code) {
        return "green";
      } else {
        return "red";
      }
    },
    checkPassword() {
      if (this.confirm_password == this.password && this.password != "") {
        return "green";
      } else {
        return "red";
      }
    },
    code() {
      return this.$store.state.users.code;
    },
    enable_email() {
      return this.$store.state.users.enable_email;
    },
  },
  mounted() {
    document.getElementById("birth").max = new Date()
      .toISOString()
      .split("T")[0];
  },
  methods: {
    changeTab(tabIndexValue) {
      if (tabIndexValue < this.active_tab || this.step >= tabIndexValue) {
        this.active_tab = tabIndexValue;
        this.step = Math.max(this.step, tabIndexValue);
      }
    },
    firstStep() {
      if (this.enable_email == false) {
        this.$store.commit("SET_MESSAGE", [
          "error",
          "Подтвердите введенный email",
        ]);
      } else if (this.checkEmail == "red") {
        this.$store.commit("SET_MESSAGE", [
          "error",
          "Введен неверный код подтверждения",
        ]);
      } else {
        this.password = "";
        this.confirm_password = "";
        this.username = "";
        this.active_tab = 1;
        this.step = 1;
      }
    },
    secondStep() {
      if (this.login == "") {
        this.$store.commit("SET_MESSAGE", ["error", "Введите логин"]);
      } else if (this.username == "") {
        this.$store.commit("SET_MESSAGE", [
          "error",
          "Введите имя пользователя",
        ]);
      } else if (this.password == "") {
        this.$store.commit("SET_MESSAGE", ["error", "Введите пароль"]);
      } else if (this.confirm_password == "" || this.checkPassword == "red") {
        this.$store.commit("SET_MESSAGE", ["error", "Подтвердите пароль"]);
      } else {
        // this.$router.push("/");
        const data = {
          login: this.login,
          email: this.email,
          username: this.username,
          password: this.password,
        };
        if (this.date_of_birth != "")
          data["date_of_birth"] = this.date_of_birth;
        console.log(data);
        this.$store.dispatch("REGISTER_USER", data);
      }
    },
    sendConfiramtion() {
      this.$store.dispatch("SEND_CONFIRMATION", this.email);
    },
  },
  data() {
    return {
      option: 0,
      index: 0,
      active_tab: 0,
      step: 0,
      email: "",
      login: "",
      username: "",
      password: "",
      birth: "",
      confirm_password: "",
      confirm_email: "",
      tabs: [
        {
          tab_title: "Первый шаг",
          tab_icon: "fa fa-bookmark",
        },
        {
          tab_title: "Второй шаг",
          tab_icon: "fa fa-comments",
        },
      ],
    };
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/register.scss";
@import "../assets/scss/user_profile.scss";
</style>
