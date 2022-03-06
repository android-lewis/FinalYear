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
        <GalleryThumb :thumbnail="data['thumbnail'] == null ? 'https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg' : data['thumbnail']" :title="data['name']" :id="data['gallery_id']" @refresh="refresh" />
      </template>
    </div>
  </div>
  <Modal v-show="state.modalVisible" @close="closeModal">
      <template v-slot:body>
        <label for="inputName">Gallery Name</label>
        <input ref="name" type="text" id="inputName" />
        <label for="inputVisibility">Public</label>
        <input ref="visibility" type="checkbox" id="inputVisibility" />
      </template>
      <template v-slot:footer>
          <button v-on:click="createGal">Create Gallery</button>
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

export default defineComponent({
  name: "Account",
  components: {
    ProfileHeader,
    SavedImageContainer,
    Modal,
    GalleryThumb
},
  setup(props:any, components:any) {
    const state = reactive({ data: [], modalVisible: false });
    const name = ref(null);
    const visibility = ref(null);
    const newGal = () => {
      showModal();
    }
    const createGal = () => {
      let postBody = {
        name: name.value,
        visibility: visibility.value == "on" ? true : false
      }

      axios.post('/api/gallery/create', postBody, {
        headers: {
          'x-access-tokens': `${sessionStorage.getItem('token')}`
        }
      }).then((response) => {
        console.log(response);
        console.log("success");
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
  });
  
  return { state, name, visibility, refresh, createGal, newGal, showModal, closeModal }
  }
})
</script>