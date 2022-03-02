<template>
  <div>
    <h1>{{ type }}</h1>
    <div class="container p-5 mx-auto mt-5 bg-gray-200 grid sm:grid-cols-3 gap-4">
      <template v-for="(data) in state.data">
        <GalleryItem :thumbnail="data['file_location']" :title="data['name']" :id="data['image_id']" @refresh="refresh"/>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import router from "@/router";
import axios from "axios";
import { defineComponent, onMounted, reactive } from "vue";
import SavedImageContainer from "@/components/profile/SavedImageContainer.vue";
import GalleryItem from "@/components/gallery/GalleryItem.vue";

export default defineComponent({
    name: "Gallery",
    props: {
        type: {
            type: String,
            required: true,
        }
    },
    components: { SavedImageContainer, GalleryItem },
    setup(props:any, components:any) {
        const type = props.type;
        const state = reactive({ data: [] })
        const refresh = () => {
          if(type != undefined){
            let path = `/api/image/${type.toLowerCase()}`
            axios.get(path, { headers: { 'x-access-tokens': `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response); state.data = response.data.value; }).catch((response) => { console.log(response) });
          }
        }
        onMounted(() => {
          refresh()
        });
        return { type, state, refresh }
    }
})
</script>