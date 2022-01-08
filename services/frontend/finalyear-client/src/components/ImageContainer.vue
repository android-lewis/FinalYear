<template>
  <div class="max-w-512 aspect-square bg-slate-600">
    <img :src="path" />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({
  props: {
    imgSrc: String,
  }
})
export default class ImageContainer extends Vue {
    imgSrc!: string;

    get path() {
        return new URL(`../assets/${this.imgSrc}`, import.meta.url);
    }
}
</script>