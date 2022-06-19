<template>
  <div id="app">
    <!-- <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </nav> -->
    <main>
      <router-view />
    </main>
    <PopupMessage :message="message" :key="key" />
    <Footer />
  </div>
</template>

<script>
import Footer from "@/components/Footer.vue";
import PopupMessage from "@/components/PopupMessage.vue";

export default {
  name: "App",
  components: {
    Footer,
    PopupMessage,
  },
  created() {
    this.$store.commit("TOKEN");
  },
  computed: {
    message() {
      this.animationStart();
      return this.$store.state.message;
    },
  },
  methods: {
    animationStart() {
      this.key += 1;
    },
  },
  data() {
    return {
      key: 0,
    };
  },
};
</script>

<style lang="scss">
@import "assets/scss/_variables.scss";



.button {
  border: $border;
  padding: 10px;
  font-weight: bold;
  background-color: transparent;
  font-size: $standart_font_size;
  cursor: pointer;
}

.head {
  margin: $short_height auto $margin;
}

body,
p {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

main {
  min-height: calc(100vh - $short_height * 1.6 - $header_full_height);
  background-color: $main_color;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

fa {
  cursor: pointer;
  font-size: 18px;
}
</style>
