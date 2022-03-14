<template>
  <div class="relative bg-white overflow-hidden">
    <main id="hero" class="px-5 py-[50px] w-screen bg-gradient-to-r from-orange-600 to-amber-500">
      <div class="sm:text-center lg:text-left">
        <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span class="block xl:inline">{{ state.gallery.name == undefined ? type : state.gallery.name }}</span>
        </h1>
      </div>
    </main>
    
    <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <template v-for="(data) in state.data">
        <GalleryItem v-if="type != undefined" :thumbnail="data['file_location']" :title="data['name']" :id="data['image_id']" @refresh="refresh" @removeGallery="removeGallery" :type="state.predefined"/>
      </template>
      <AddNewItem v-show="!state.predefined" v-on:click="showModal"/>
    </div>
  </div>
  <Modal v-show="state.modalVisible" @close="closeModal">
      <template v-slot:header>
        <h1>Add Images to Gallery</h1>
      </template>
      <template v-slot:body>
        <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <template v-for="(data, i) in state.allImages" :key="state.data.length">
            <div class="flex flex-col">
              <input type="checkbox" :id="data.image_id" @change="updateChecked"/>
              <label :for="data.image_id" :class="getClass"><img :src="data.file_location" alt="image thumb" class="max-w-sm bg-white border border-gray-200 shadow-md col-span-1"/></label>
            </div>
          </template>
        </div>
      </template>
      <template v-slot:footer>
          <button v-on:click="addToGal" class="w-full bg-orange-600 hover:bg-orange-400 text-white font-bold font-body py-6 px-auto text-2xl">Add to Gallery</button>
      </template>
  </Modal>
</template>
<style scoped lang="scss">

input[type="checkbox"] {
  display: none;
}

label {
  border: 2px solid orangered;
  padding: 10px;
  display: block;
  position: relative;
  margin: 10px;
  cursor: pointer;
}

label:before {
  background-color: white;
  color: white;
  content: " ";
  display: block;
  border-radius: 50%;
  border: 2px solid orangered;
  position: absolute;
  top: -5px;
  left: -5px;
  width: 25px;
  height: 25px;
  text-align: center;
  line-height: 28px;
  transition-duration: 0.2s;
  transform: scale(0);
}

label img {
  height: 250px;
  width: 250px;
  transition-duration: 0.1s;
  transform-origin: 50% 50%;
}

:checked + label {
  border-color: #ddd;
}

:checked + label:before {
  background-color: orangered;
  transform: scale(1);
}

:checked + label img {
  transform: scale(0.9);
  /* box-shadow: 0 0 5px #333; */
  z-index: -1;
}

.alreadyin {
  border-color: blue
}

</style>
<script lang="ts">
import router from "@/router";
import axios from "axios";
import { defineComponent, onMounted, onBeforeUpdate, reactive, ref, watch } from "vue";
import SavedImageContainer from "@/components/profile/SavedImageContainer.vue";
import GalleryItem from "@/components/gallery/GalleryItem.vue";
import GalleryThumb from "@/components/gallery/GalleryThumb.vue";
import AddNewItem from "@/components/gallery/AddNewItem.vue";
import Modal from "@/components/modal/Modal.vue";
import { onBeforeRouteLeave } from "vue-router";



export default defineComponent({
    name: "Gallery",
    props: {
        type: {
            type: String,
            required: false,
        }
    },
    components: { SavedImageContainer, GalleryItem, GalleryThumb, AddNewItem, Modal },
    setup(props:any, components:any) {
        type ImageMap = { id: string, status: Boolean };
        type Gallery = {description: string , gallery_id: string , name: string, owner_id: number, thumbnail: string, visibility: boolean}
        let map : ImageMap[]; 
        const type = ref(props.type);
        watch(props.type, (newType, oldType) => { console.log(newType + " : " + oldType) });
        const state = reactive({ data: [], allImages: [] as Array<{ file_location: string, name: string, image_id: string, checked: Boolean }>, predefined: false, modalVisible: false, gallery: {} as Gallery, galleries: [] as Array<Gallery> })
        const refresh = () => {
          let acceptedTypes = ["Generated", "Uploaded", "Combined"];
          if(type.value != undefined && acceptedTypes.includes(type.value) == true){
            state.predefined = true;
            let path = `/api/image/${type.value.toLowerCase()}`
            axios.get(path, { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response); state.data = response.data.value; }).catch((response) => { console.log(response) });
          
          } else if (type.value != undefined && acceptedTypes.includes(type.value) == false) {
            getGallery();
            let path = `/api/image/gallery?galleryid=${type.value}`
            
            axios.get(path, { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response); state.data = response.data.value; }).catch((response) => { console.log(response) });
            
            axios.get("/api/image/combined", { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }})
            .then((response) => { console.log(response); state.allImages = response.data.value })
            .catch((response) => { console.log(response) });
          }
        }

        const getClass = (e:any) => {
          console.log(e.target);
          return 'alreadyin'
        }
        const updateChecked = (e:any) => {

          console.log(e.target.id);
          console.log(e.target.checked);

          let temp: ImageMap = { id: e.target.id, status: e.target.checked }

          if(map.filter(e => e.id === temp.id).length > 0){
            map = map.filter(item => item.id != temp.id);
            map.push(temp);
          } else {
            map.push(temp);
          }
        }

        const addToGal = () => {
          map.forEach(element => {
            if (element.status == true) {
              const postData = {
                "image_id" : element.id,
                "gallery_id": type.value
              }

              axios.patch("/api/image/modify", postData, { headers: {
                'x-access-tokens': `${sessionStorage.getItem('token')}`
              }}).then((response) => {
                    console.log(response);
                    console.log("success");
                  }).catch((response) => {
                    console.log(response)
                    console.log("failed");
                })
            }
          });

          refresh();
        }

        onBeforeRouteLeave(() => {
          console.log(type.value);
          console.log(state)
        })

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

        const removeGallery = (id:string) => {
          const postData = {
                "image_id" : id,
                "gallery_id": null
              }

          axios.patch("/api/image/modify", postData, { headers: {
            'x-access-tokens': `${sessionStorage.getItem('token')}`
          }}).then((response) => {
                console.log(response);
                console.log("success");
                refresh();
              }).catch((response) => {
                console.log(response)
                console.log("failed");
          })
        }

        const getGallery = () => {

          axios.get("/api/gallery/get", { params: {
            "galleryid": type.value
          }}).then((response) => {
            state.gallery = response.data.value;
          }).catch((response) => {
            console.log(response)
            state.gallery = { description: "null",
                              gallery_id: "null",
                              name: "There was an issue",
                              owner_id: -1,
                              thumbnail: "null",
                              visibility: false };
          })
        }

        onMounted(() => {
          refresh();
        });

        return { type, state, refresh, removeGallery, viewImages, showModal, closeModal, addToGal, updateChecked, getClass }
    }
})
</script>