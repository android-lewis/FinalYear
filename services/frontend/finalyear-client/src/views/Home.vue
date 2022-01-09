<template>
  <div class="w-screen h-full flex flex-col mx-auto justify-center items-center p-10">
    <div class="container mx-auto space-y-2 lg:space-y-0 lg:gap-2 lg:grid lg:grid-cols-2">
      <ImageContainer imgSrc="logo.png" />
      <ImageContainer />
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
