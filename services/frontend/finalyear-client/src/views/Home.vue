<template>
  <Loading v-model:active="isLoading"
                  can-cancel="false"
                  is-full-page="true"/>
  <div class="w-screen h-full flex flex-col mx-auto justify-center items-center p-10">
    <div class="container mx-auto space-y-2 lg:space-y-0 lg:gap-2 lg:grid lg:grid-cols-2">
      <ImageContainer role="upload" />
      <ImageContainer role="gen" />
    </div>
    <div class="container flex flex-col">
      <div>
        <label for="strengthRange" class="form-label">Strength</label>
        <input
          type="range"
          class="
            form-range
            appearance-none
            w-full
            h-6
            p-0
            bg-transparent
            focus:outline-none focus:ring-0 focus:shadow-none
          "
          min="0.0"
          max="1.0"
          step="0.1"
          id="strengthRange"
          v-model="strength"
        />
      </div>
      <div>
        <button v-on:click="stylize" class="w-full bg-orange-600 hover:bg-orange-400 text-white font-bold font-body py-6 px-auto text-2xl">Combine</button>
      </div>
    </div>
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
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
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
    Loading,
  },
})
export default class Home extends Vue {
  $refs!: {
    canvas: HTMLCanvasElement
  }

  isLoading:Boolean = false;
  refCount:number = 0;
  strength:string = "0.9";
  modalVisible:Boolean = false;
  model:any = new mi.ArbitraryStyleTransferNetwork();

  setLoading(loading:boolean){
    if (loading) {
        this.refCount++;
        this.isLoading = true;
        console.log(this.isLoading);
      } else if (this.refCount > 0) {
        this.refCount--;
        this.isLoading = (this.refCount > 0);
      }
  }

  stylize() {
    this.setLoading(true);
    console.log("Loading...");
    this.model.initialize().then(this.styleImage);
  }
  
  styleImage(){
    const {state} = global;
    let uploadImage = new Image(512,512);
    let genImage = new Image(512,512);
    let raw_model = toRaw(this.model);

    
    uploadImage.src = state.uploadImageURL;
    genImage.src = state.genImageURL;

    raw_model.stylize(uploadImage, genImage, parseFloat(this.strength)).then((imageData: any) => {
      if(!(this.$refs.canvas instanceof HTMLCanvasElement)){
        throw new Error('The element is not a HTMLCanvasElement.');
      } else {
        const ctx = getCanvasRenderingContext2D(this.$refs.canvas);
        if(ctx){
          ctx.putImageData(imageData, 0, 0);
          this.setLoading(false);
          console.log("Finished loading");
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
