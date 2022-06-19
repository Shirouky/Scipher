<template>
  <div>
    <div class="tags">
      <div v-for="user in users" :key="user.id" class="tag">
        <img
          class="avatar"
          :src="`data:image/jpeg;base64,${user.avatar ? user.avatar : ''}`"
        />
        <a :style="{ color: user.text_color }">{{ user.username }}</a>
        <fa @click="deleteUser(user)" class="trash" icon="fa-solid fa-trash" />
      </div>
    </div>
    <div class="input_container">
      <input
        @input="searchUser()"
        type="text"
        class="input-search"
        placeholder="Укажите пользователя"
        v-model="user_input"
      />
      <ul class="submenu">
        <li v-for="user in user_search" :key="user.id" @click="addUser(user)">
          <p>{{ user.username }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchUser",
  props: {
    mode: String,
    users: Array,
  },
  computed: {
    user_search() {
      return this.$store.state.users.user_search;
    },
  },
  methods: {
    searchUser() {
      this.$store.dispatch("SEARCH_USER", this.user_input);
    },
    addUser(user) {
      this.$emit("add", user);
    },
    deleteUser(user) {
      this.$emit("remove", user);
    },
  },
  data() {
    return {
      user_input: "",
      users_display: [],
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/article_tag.scss"></style>
