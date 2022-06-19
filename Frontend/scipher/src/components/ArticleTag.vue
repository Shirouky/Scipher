<template>
  <div>
    <div class="tags">
      <div
        v-for="tag in tags_display"
        :key="tag.id"
        class="tag"
        :style="{ 'background-color': tag.background_color }"
      >
        <a
          :style="{ color: tag.text_color }"
          @click="$router.push(`/tag/${tag.id}`)"
          >{{ tag.title }}</a
        >
        <fa
          v-if="edit_mode || edit"
          @click="deleteTag(tag)"
          class="trash"
          icon="fa-solid fa-trash"
        />
      </div>
      <fa
        v-if="tags && shorten && tags.length > len"
        @click="changeDisplay()"
        class="fa-xl fa"
        icon="fa-solid fa-ellipsis"
      />
      <fa
        v-if="!edit_mode && enable"
        @click="edit_mode = true"
        icon="fa-solid fa-pen-to-square"
      />
    </div>
    <div class="input_container" v-if="edit || edit_mode">
      <input
        @input="searchTag()"
        type="text"
        class="input-search"
        placeholder="Укажите тег"
        v-model="tag_input"
      /><fa
        v-if="times"
        @click="disable()"
        class="fa-xl"
        icon="fa-solid fa-times"
      />
      <ul class="submenu">
        <li v-for="tag in tag_search" :key="tag.id" @click="addTag(tag)">
          <p>{{ tag.title }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "ArticleTag",
  props: {
    mode: String,
    tags: Array,
  },
  computed: {
    tag_search() {
      return this.$store.state.tags.tag_search;
    },
  },
  mounted() {
    if (this.mode == "search") {
      this.times = false;
      this.enable = false;
      this.edit = true;
      this.shorten = true;
    }
    if (this.mode == "full_article") {
      this.times = false;
      this.enable = false;
      this.edit = false;
      this.shorten = true;
    }
    if (this.mode == "short_article") {
      this.times = false;
      this.enable = false;
      this.edit = false;
      this.shorten = this.tags && this.tags.length <= this.len;
    }
    if (this.mode == "edit_article") {
      this.times = false;
      this.enable = false;
      this.edit = true;
      this.shorten = true;
    }
    this.changeDisplay();
  },
  methods: {
    searchTag() {
      this.$store.dispatch("SEARCH_TAG", this.tag_input);
    },
    addTag(tag) {
      this.$emit("add", tag);
    },
    deleteTag(tag) {
      this.$emit("remove", tag);
    },
    changeDisplay() {
      this.shorten = !this.shorten;
      if (this.shorten) {
        this.tags_display = this.tags.slice(0, this.len);
      } else {
        this.tags_display = this.tags;
      }
    },
  },
  data() {
    return {
      edit: true,
      tag_input: "",
      tags_display: [],
      edit_mode: false,
      shorten: true,
      enable: true,
      times: true,
      len: 5,
    };
  },
};
</script>


<style scoped lang="scss" src="../assets/scss/article_tag.scss"></style>
