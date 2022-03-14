<template>
  <div class="flex flex-col content-center">
    <ProfileHeader />
    <div class="container p-5 mx-auto my-5 bg-gray-200 grid sm:grid-cols-3 gap-4">
      <SavedImageContainer thumbnail="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg" title="Uploaded" />
      <SavedImageContainer thumbnail="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg" title="Generated" />
      <SavedImageContainer thumbnail="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg" title="Combined" />
    </div>
    <div class="container h-16 p-5 bg-gray-200 flex justify-between flex-row mx-auto">
      <h1>Galleries</h1>
      <div>
        <button v-on:click="newGal">Add New Gallery</button>
      </div>
    </div>
    <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <template v-for="(data) in state.data">
        <GalleryThumb :thumbnail="data['thumbnail'] == null ? 'https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg' : data['thumbnail']" :title="data['name']" :id="data['gallery_id']" :controls="true" @refresh="refresh" />
      </template>
    </div>
  </div>
  <Modal v-show="state.modalVisible" @close="closeModal">
      <template v-slot:header>
        <h1>New Gallery</h1>
      </template>
      <template v-slot:body>
        <div class="w-full max-w-xs flex flex-col">
          <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <label for="inputName" class="block text-gray-700 text-sm font-bold mb-2">Gallery Name</label>
            <input v-model="state.nameval" type="text" id="inputName" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          </div>  
          <div class="md:flex md:items-center mb-6">
            <label class="md:w-3/3 block text-gray-500 font-bold">
              <input class="mr-2 leading-tight" v-model="state.visibility" type="checkbox" id="inputVisibility">
              <span class="text-sm">
                Public Gallery
              </span>
            </label>
          </div>
        </div>
      </template>
      <template v-slot:footer>
          <button v-on:click="createGal" class="w-full bg-orange-600 hover:bg-orange-400 text-white font-bold font-body py-6 px-auto text-2xl">Create Gallery</button>
      </template>
  </Modal>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from "vue";
import axios from "axios";
import global from "../composables/global";
import ProfileHeader from "@/components/profile/ProfileHeader.vue"
import SavedImageContainer from "@/components/profile/SavedImageContainer.vue";
import Modal from "@/components/modal/Modal.vue";
import GalleryThumb from "@/components/gallery/GalleryThumb.vue";
import { notify } from "@kyvg/vue3-notification";

export default defineComponent({
  name: "Account",
  components: {
    ProfileHeader,
    SavedImageContainer,
    Modal,
    GalleryThumb
},
  setup(props:any, components:any) {
    const state = reactive({ data: [], modalVisible: false, nameval: "", visibility: false });
    const newGal = () => {
      showModal();
    }
    const createGal = () => {
      let postBody = {
        name: state.nameval,
        visibility: state.visibility
      }
      console.log(state);
      console.log(postBody);

      axios.post('/api/gallery/create', postBody, {
        headers: {
          'x-access-tokens': `${sessionStorage.getItem('token')}`
        }
      }).then((response) => {
        console.log(response);
        console.log("success");
        refresh();
      }).catch((response) => {
        console.log(response)
        console.log("failed");
      })
  }

  const showModal = () => {
    state.modalVisible = true;
  };

  const closeModal = () => {
    state.modalVisible = false;
  };

  const refresh = () => {
      notify({
        title: "Vue 3 notification 🎉",
      });
      axios.get('/api/gallery/', {
        headers: {
          'x-access-tokens': `${sessionStorage.getItem('token')}`
        }
      }).then((response) => {
        console.log(response);
        state.data = response.data.value;
        console.log("success");
      }).catch((response) => {
        console.log(response)
        console.log("failed");
      })
  }

  onMounted(() => {
    refresh()
    notify({
      title: "Vue 3 notification 🎉",
    });
  });
  
  return { state, refresh, createGal, newGal, showModal, closeModal }
  }
})
</script>