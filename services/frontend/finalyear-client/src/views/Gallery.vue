<template>
  <div class="relative bg-white overflow-hidden">
    <main id="hero" class="px-5 py-[50px] w-screen bg-gradient-to-r from-orange-600 to-amber-500">
      <div class="sm:text-center lg:text-left">
        <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span class="block xl:inline">{{type}}</span>
        </h1>
      </div>
    </main>
    
    <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <template v-for="(data) in state.data">
        <GalleryItem :thumbnail="data['file_location']" :title="data['name']" :id="data['image_id']" @refresh="refresh" @gallery="addGallery" :type="state.predefined"/>
      </template>
      <AddNewItem v-show="!state.predefined" v-on:click="showModal"/>
    </div>
  </div>
  <Modal v-show="state.modalVisible" @close="closeModal">
      <template v-slot:body>
        <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <template v-for="(data, i) in state.allImages">
            <div class="flex flex-col">
              <GalleryItem :thumbnail="data.file_location" :title="data.name" :id="data.image_id" @refresh="refresh" @gallery="addGallery" :type="state.predefined"/>
              <label :for="data.image_id">Select Image</label>
              <input type="checkbox" :id="data.image_id" @change="updateChecked"/>
            </div>
          </template>
        </div>
      </template>
      <template v-slot:footer>
          <button v-on:click="addToGal">Add to Gallery</button>
      </template>
  </Modal>
</template>
<script lang="ts">
import router from "@/router";
import axios from "axios";
import { defineComponent, onMounted, onBeforeUpdate, reactive, ref } from "vue";
import SavedImageContainer from "@/components/profile/SavedImageContainer.vue";
import GalleryItem from "@/components/gallery/GalleryItem.vue";
import AddNewItem from "@/components/gallery/AddNewItem.vue";
import Modal from "@/components/modal/Modal.vue";



export default defineComponent({
    name: "Gallery",
    props: {
        type: {
            type: String,
            required: true,
        }
    },
    components: { SavedImageContainer, GalleryItem, AddNewItem, Modal },
    setup(props:any, components:any) {
        type ImageMap = { id: string, status: Boolean };
        let map : ImageMap[]; 
        const type = props.type;
        const state = reactive({ data: [], allImages: [] as Array<{ file_location: string, name: string, image_id: string, checked: Boolean }>, predefined: false, modalVisible: false })
        const refresh = () => {
          let acceptedTypes = ["Generated", "Uploaded", "Combined"];
          if(type != undefined && acceptedTypes.includes(type) == true){
            state.predefined = true;
            
            let path = `/api/image/${type.toLowerCase()}`
          
            axios.get(path, { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response); state.data = response.data.value; }).catch((response) => { console.log(response) });
          
          } else if (type != undefined && acceptedTypes.includes(type) == false) {
            
            let path = `/api/image/gallery?galleryid=${type}`
            
            axios.get(path, { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response); state.data = response.data.value; }).catch((response) => { console.log(response) });
            
            axios.get("/api/image/combined", { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }})
            .then((response) => { console.log(response); state.allImages = response.data.value })
            .catch((response) => { console.log(response) });
          }
        }

        const updateChecked = (e:any) => {
          console.log(e.target.id);
          console.log(e.target.value);

          let temp: ImageMap = { id: e.target.id, status: e.target.value == "on" ? true : false }

          if(map.filter(e => e.id === temp.id).length > 0){
            map.filter(item => item.id == temp.id);
          } else {
            map.push(temp);
          }
        }

        const addToGal = () => {
          console.log(map);
        }

        onBeforeUpdate(() => {
          map = []
        })

        const viewImages = () => {
          showModal();
        }

        const showModal = () => {
          state.modalVisible = true;
        };

        const closeModal = () => {
          state.modalVisible = false;
        };

        const addGallery = (id:string) => {
          console.log(id);
        }
        onMounted(() => {
          refresh()
        });
        return { type, state, refresh, addGallery, viewImages, showModal, closeModal, addToGal, updateChecked }
    }
})
</script>