<template>
  <div class="w-screen h-full flex flex-col mx-auto justify-center items-center p-10">
    <div class="container mx-auto space-y-2 lg:space-y-0 lg:gap-2 lg:grid lg:grid-cols-2">
      <ImageContainer role="upload" />
      <ImageContainer role="gen" />
    </div>
    <button v-on:click="stylize" class="w-full bg-orange-600 hover:bg-orange-400 text-white font-bold font-body py-4 px-4">Combine</button>
    <Modal v-show="modalVisible" @close="closeModal">
      <template v-slot:body>
        <canvas ref="canvas" id="combinedImg" height="512" width="512"></canvas>
      </template>
      <template v-slot:footer>
          <button v-on:click="saveStyled">Save Styled image</button>
      </template>
    </Modal>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { toRaw } from "vue";
import axios from 'axios';
import ImageContainer from "@/components/ImageContainer.vue"; // @ is an alias to /src
import Modal from "@/components/modal/Modal.vue";
import * as mi from '@magenta/image';
import global from "@/composables/global";
const getCanvasRenderingContext2D = (canvas: HTMLCanvasElement): CanvasRenderingContext2D => {
    const context = canvas.getContext('2d');
    if (context === null) {
        throw new Error('This browser does not support 2-dimensional canvas rendering contexts.');
    }
    return context;
};

@Options({
  components: {
    ImageContainer,
    Modal,
  },
})
export default class Home extends Vue {
  $refs!: {
    canvas: HTMLCanvasElement
  }

  modalVisible:Boolean = false;
  model:any = new mi.ArbitraryStyleTransferNetwork();

  stylize() {
    this.model.initialize().then(this.styleImage);
  }
  
  styleImage(){
    const {state} = global;
    let uploadImage = new Image(512,512);
    
    let genImage = new Image(512,512);
    let raw_model = toRaw(this.model);
    
    uploadImage.src = state.uploadImageURL;
    genImage.src = state.genImageURL;

    raw_model.stylize(uploadImage, genImage).then((imageData: any) => {
      if(!(this.$refs.canvas instanceof HTMLCanvasElement)){
        throw new Error('The element is not a HTMLCanvasElement.');
      } else {
        const ctx = getCanvasRenderingContext2D(this.$refs.canvas);
        if(ctx){
          ctx.putImageData(imageData, 0, 0);
          this.showModal()
        }
      }
    })
  }

  saveStyled() {
    
    let formData = new FormData();
    formData.append('file', this.$refs.canvas.toDataURL('image/png'));
    axios.post('/api/image/save',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
        'x-access-tokens': `${sessionStorage.getItem('token')}`
      }
    }).then((response) => {
          console.log("SUCCESS!!");
          console.log(response)
      })
      .catch((response) => {
        console.log('FAILURE!!');
        console.log(response)
    })
  }

  showModal() {
    this.modalVisible = true;
  };

  closeModal() {
    this.modalVisible = false;
  };
}
</script>
