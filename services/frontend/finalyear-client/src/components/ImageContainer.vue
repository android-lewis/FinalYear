<template>
  <div class="max-w-full aspect-square bg-gray-200">
    <template v-if="currentRole === 'upload' && uploadImgPath != ''">
      <img v-if="uploadImgPath != ''" :src="uploadImgPath" class="object-cover w-full h-auto" alt="uploaded image"/>
    </template>
    <template v-else-if="currentRole === 'gen' && genImgPath != ''">
      <img v-if="genImgPath != ''" :src="genImgPath" class="object-cover w-full h-auto" alt="generated image"/>
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
    let file_location = "";
    let data = {
      "owner_id": "1"
    };

    axios.post('/api/image/generate', 
    data, {
    headers: {
        'Content-Type': 'application/json'
    }
    }).then(function(response) {
        console.log(response.data.value.file_location);
        setGenImageURL("/images/test/" + response.data.value.file_location);
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
        },
        params: {
          'owner': '1'
        }
      }).then((response) => {
            //this.imgSrc = response.data
            console.log("SUCCESS!!");
            //console.log(response);
            console.log(response.data.value.file_location);
            setUploadImageURL(response.data.value.file_location);
        })
        .catch(function(){
          console.log('FAILURE!!');
      })
    }
  }
}
</script>