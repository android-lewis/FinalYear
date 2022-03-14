<template>
  <div class="relative bg-white overflow-hidden">
    <main id="hero" class="px-5 py-[50px] w-screen bg-gradient-to-r from-orange-600 to-amber-500">
      <div class="sm:text-center lg:text-left">
        <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span class="block xl:inline">Showcase</span>
        </h1>
      </div>
    </main>
    
    <div class="container p-5 mx-auto mt-5 bg-white grid sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <template v-for="(data) in state.data">
        <GalleryThumb :thumbnail="data['thumbnail'] == null ? 'https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg' : data['thumbnail']" :title="data['name']" :id="data['gallery_id']" :controls="false" @refresh="refresh" />
      </template>
    </div>
  </div>
</template>
<script lang="ts">
import axios from "axios";
import { defineComponent, onMounted, reactive } from "vue";
import GalleryThumb from "@/components/gallery/GalleryThumb.vue";

export default defineComponent({
    name: "Showcase",
    components: { GalleryThumb },
    setup(props:any, components:any) {
        type Gallery = {description: string , gallery_id: string , name: string, owner_id: number, thumbnail: string, visibility: boolean}
        const state = reactive({ data: [] as Array<Gallery> })
        const refresh = () => {
          getShowcase();
        }

        const getShowcase = () => {
          axios.get("/api/gallery/showcase").then((response) => { console.log(response); state.data = response.data.value }).catch((response) => { console.log(response) });
        }

        onMounted(() => {
            getShowcase();
        })

        return { state, refresh }
    }
})
</script>