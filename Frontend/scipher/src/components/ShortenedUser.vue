<template>
  <div class="container">
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
          <span @click="$router.push(`/user/${user.id}`)" class="header">
            <div class="authors">
              <img
                class="avatar"
                :src="`data:image/jpeg;base64,${
                  user.avatar ? user.avatar : ''
                }`"
              />
              <h5 class="title">
                {{ user.username }}
              </h5>
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShortenedUser",
  props: {
    user: Object,
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/shortened_article.scss"></style>
