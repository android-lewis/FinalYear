<template>
  <div class="max-w-full aspect-square bg-gray-200">
    <template v-if="currentRole === 'upload' && uploadImgPath != ''">
      <div class="w-full h-full flex items-center justify-center"><img v-if="uploadImgPath != ''" :src="uploadImgPath" class="object-cover w-full h-auto" alt="uploaded image"/></div>
      <div class="grid sm:grid-cols-2 gap-4 my-5">
        <div class="flex justify-start gap-2 col-span-1">
          <label for="upload-photo" class="bg-orange-600 hover:bg-orange-400 text-white w-[50%] font-bold font-body py-4 px-4 flex justify-center">Re-Upload</label>
          <button v-on:click="saveUplImage" class="bg-orange-600 hover:bg-orange-400 text-white w-[50%] font-bold font-body py-4 px-4">Save</button>
        </div>
        <div class="w-full col-span-1">
          <input ref="fileInput" type="file" name="photo" id="upload-photo" v-on:change="handleFileUpload"/> 
        </div>
      </div>
    </template>
    <template v-else-if="currentRole === 'gen' && genImgPath != ''">
      <img v-if="genImgPath != ''" :src="genImgPath" class="object-cover w-full h-auto" alt="generated image"/>
      <div class="grid sm:grid-cols-2 gap-4 my-5">
        <div class="flex justify-start gap-2 col-span-1">
          <button v-on:click="genNewImage" class="bg-orange-600 hover:bg-orange-400 text-white w-[50%] font-bold font-body py-4 px-4">Regenerate</button>
          <button v-on:click="saveGenImage" class="bg-orange-600 hover:bg-orange-400 text-white w-[50%] font-bold font-body py-4 px-4">Save</button>
        </div>
        <div class="w-full col-span-1"></div>
      </div>
    </template>
    <template v-else-if="uploadImgPath === '' && currentRole === 'upload'">
      <label for="upload-photo" class="w-full h-full flex items-center justify-center hover:bg-gray-300 transition duration-500"><img :src="uploadIconPath" class="object-contain w-[25%] h-auto" alt="Upload image icon" /></label>
      <input ref="fileInput" type="file" name="photo" id="upload-photo" v-on:change="handleFileUpload" />
    </template>
    <template v-else-if="genImgPath === '' && currentRole === 'gen'">
        <button v-on:click="genNewImage">Generate</button>
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
import global from "../composables/global";

@Options({
  props: {
    role: String,
  }
})
export default class ImageContainer extends Vue {
  imgSrc!: string;
  role!: string;
  $refs!: {
    fileInput: HTMLInputElement
  }

  reset(){
    const {setUploadImageURL} = global;
    setUploadImageURL("");
  }

  get currentRole(){
    return this.role;
  }

  get genImgPath(){
    const { state } = global;
    return state.genImageURL;
    //return new URL("../assets/image-items/upload.svg", import.meta.url).href
  }

  genNewImage() {
    const { setGenImageURL } = global;

    axios.post('/api/image/generate', 
    {
    headers: {
        'Content-Type': 'application/json'
    }
    }).then(function(response) {
        setGenImageURL(response.data.value);
    })
    .catch(function(){
        console.log('FAILURE!!');
    })
  }

  saveGenImage() {
    let postData = {
      src: this.genImgPath
    }

    axios.post('/api/image/saveGenerated', 
    postData,
    {
      headers: {
        "x-access-tokens": `${sessionStorage.getItem('token')}`
      }
    }).then((response) => {
            console.log("SUCCESS!!");
            console.log(response)
        })
        .catch(function(){
          console.log('FAILURE!!');
      })
  }

  get uploadIconPath() {
    return new URL("../assets/image-items/upload.svg", import.meta.url).href;
  }

  get uploadImgPath() {
    const { state } = global;
    return state.uploadImageURL;
  }

  handleFileUpload() {
    const { setUploadImageURL } = global;
    let formData = new FormData();
    let file = this.$refs.fileInput;
    if(file.files != null){
      formData.append('file', file.files[0]);
      axios.post('/api/image/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
            console.log("SUCCESS!!");
            setUploadImageURL(response.data.value);
        })
        .catch(function(){
          console.log('FAILURE!!');
      })
    }
  }

  saveUplImage() {
    let postData = {
      src: this.uploadImgPath
    }

    axios.post('/api/image/saveUploaded', 
    postData,
    {
      headers: {
        "x-access-tokens": `${sessionStorage.getItem('token')}`
      }
    }).then((response) => {
            console.log("SUCCESS!!");
            console.log(response)
        })
        .catch(function(){
          console.log('FAILURE!!');
      })
  }
}
</script>