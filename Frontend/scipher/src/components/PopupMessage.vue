<template>
  <div
    :class="[fade, message.type]"
    :style="{ display: display }"
    class="container"
  >
    <p>{{ message.text }}</p>
  </div>
</template>

<script>
export default {
  name: "PopupMessage",
  props: {
    message: Object,
  },
  mounted() {
    setTimeout(() => {
      this.fade = "fade-out";
      setTimeout(() => {
        this.display = "none";
      }, 300);
    }, 5000);
  },
  data() {
    return {
      fade: "fade-in",
      display: "block",
    };
  },
};
</script>


<style scoped lang="scss">
@import "../assets/scss/_variables.scss";
$animation: fadeIn ease 0.5s;
.fade-in {
  animation: $animation;
  -webkit-animation: $animation;
  -moz-animation: $animation;
  -o-animation: $animation;
  -ms-animation: $animation;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@-moz-keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@-webkit-keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@-o-keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@-ms-keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

$animation: fadeOut ease 0.5s;
.fade-out {
  animation: $animation;
  -webkit-animation: $animation;
  -moz-animation: $animation;
  -o-animation: $animation;
  -ms-animation: $animation;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-moz-keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-webkit-keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-o-keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@-ms-keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.container {
  position: fixed;
  bottom: 20px;
  width: 300px;
  max-width: 100vw;
  padding: 10px;
  border-radius: 10px;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
}

.error {
  background-color: $light_red;
  border: 1px solid $red;
}

.message {
  background-color: $light_green;
  border: 1px solid $green;
}
</style>
