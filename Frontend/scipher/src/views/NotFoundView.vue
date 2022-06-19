<template>
  <div>
    <FullHeader />
    <div class="head">
      <h2>404! Страница не найдена</h2>
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import FullHeader from "@/components/FullHeader.vue";

export default {
  name: "NotFoundView",
  components: {
    FullHeader,
  },
};
</script>

<style scoped lang="scss">
@import "../assets/scss/_variables.scss";

.head {
  margin: $header_full_height auto;
  text-align: center;
  padding: 30vh 0 20px;
}
</style>
