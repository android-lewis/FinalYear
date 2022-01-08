<template>
  <div class="w-screen flex flex-col mx-auto">
    <div class="container flex">
      <ImageContainer imgSrc="logo.png" />
      <ImageContainer imgSrc="logo.png" />
    </div>
    
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import ImageContainer from "@/components/ImageContainer.vue"; // @ is an alias to /src

@Options({
  components: {
    ImageContainer,
  },
})
export default class Home extends Vue {}
</script>
