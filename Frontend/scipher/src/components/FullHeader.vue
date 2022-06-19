<template>
  <header id="masthead" class="full">
    <div class="container">
      <h1 id="shadow">Scipher</h1>
      <h2 id="title" @click="$router.push('/')">Scipher</h2>
      <nav>
        <Search />
        <div class="margin">
          <UserMenu :user="user" />
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import Search from "@/components/Search.vue";
import UserMenu from "@/components/UserMenu.vue";

export default {
  name: "FullHeader",
  components: {
    Search,
    UserMenu,
  },
  created() {
    this.prevScrollpos = window.pageYOffset;
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    handleScroll() {
      var currentScrollPos = window.pageYOffset;
      const nav = document.getElementById("masthead");
      const title = document.getElementById("title");
      const shadow = document.getElementById("shadow");

      if (currentScrollPos < 140) {
        title.style.fontSize = "50px";
        title.style.marginTop = String(130 - currentScrollPos) + "px";
        shadow.style.marginTop = String(80 - currentScrollPos) + "px";
        nav.style.height = String(200 - currentScrollPos) + "px";
      } else {
        title.style.marginTop = "10px";
        title.style.fontSize = "30px";
        nav.style.height = "60px";
      }

      if (currentScrollPos < 100) {
        shadow.style.display = "inline";
      } else {
        shadow.style.display = "none";
      }
    },

    changeLanguage(lang) {
      this.$cookies.set("language", lang, "session");
      window.location.reload();
    },
  },
  data() {
    return {
      lang: {},
      user: {
        id: 2,
        avatar:
          "https://www.sunhome.ru/i/wallpapers/163/alberta-banf-kanada.1920x1200.jpg",
        username: "sdfsdf",
      },
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/header.scss"></style>
