<template>
  <div class="max-w-full aspect-square bg-gray-200">
    <img v-if="path != null" :src="path" class="object-contain w-full h-auto" alt="image"/>
    <template v-else-if="path === null">
      <label for="upload-photo" class="w-full h-full flex items-center justify-center hover:bg-gray-300 transition duration-500"><img :src="uploadIconPath" class="object-contain w-[25%] h-auto" alt="Upload image icon" /></label>
      <input ref="fileInput" type="file" name="photo" id="upload-photo" v-on:change="handleFileUpload" />
    </template>
  </div>
</template>
<style>
  label {
    cursor: pointer;
  }
  #upload-photo {
   opacity: 0;
   position: absolute;
   z-index: -1;
}
</style>
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import axios from "axios";

@Options({
  props: {
    imgSrc: String,
  }
})
export default class ImageContainer extends Vue {
  imgSrc!: string;
  $refs!: {
    fileInput: HTMLInputElement
  }

  get uploadIconPath() {
    return new URL("../assets/image-items/upload.svg", import.meta.url).href;
  }

  get path() {
    console.log(this.imgSrc)
    if(this.imgSrc != undefined){ return new URL(`../assets/${this.imgSrc}`, import.meta.url).href; } 
    else{ return null; }
    return null  
  }

  handleFileUpload() {

    let formData = new FormData();
    let file = this.$refs.fileInput;
    if(file.files != null){
      formData.append('file', file.files[0]);
      axios.post('/api/image/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        params: {
          'owner': '1'
        }
      }).then(function(){
            console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
      })
    }
  }
}
</script>