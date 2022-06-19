<template>
  <div>
    <FullHeader color="#0033ff" header="Scipher" />
    <div class="home">
      <h3>Найденные пользователи</h3>
      <div class="container">
        <ShortenedUser
          v-for="user in user_search"
          :key="user.id"
          :user="user"
        />
      </div>
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import FullHeader from "@/components/FullHeader.vue";
import ShortenedUser from "@/components/ShortenedUser.vue";

export default {
  name: "SearchView",
  components: {
    FullHeader,
    ShortenedUser,
  },
  computed: {
    user_search() {
      return this.$store.state.users.user_search;
    },
  },
};
</script>

<style scoped lang="scss" src="../assets/scss/search_view.scss"></style>
