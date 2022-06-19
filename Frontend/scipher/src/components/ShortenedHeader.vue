<template>
  <header id="masthead" class="scrolled">
    <div class="container">
      <h2 id="title" @click="$router.push('/')">Scipher</h2>
      <nav>
        <Search />
        <div class="margin">
          <UserMenu />
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import Search from "@/components/Search.vue";
import UserMenu from "@/components/UserMenu.vue";

export default {
  name: "HeadComponent",
  components: {
    Search,
    UserMenu,
  },
  data() {
    return {};
  },
};
</script>
<style scoped lang="scss" src="../assets/scss/header.scss"></style>