<template>
  <Loading v-model:active="isLoading"
                  can-cancel="false"
                  is-full-page="true"/>
  <nav class="sticky top-0 w-screen max-h-100 flex justify-around mx-auto bg-zinc-900">
    <div class="items-center flex flex-row flex-nowrap">
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/gallery" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/image-nav.svg" alt="Image Icon for Gallery Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/camera-nav.svg" alt="Camera Icon for Home Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/account" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/user-nav.svg" alt="Profile Icon for Account Page"/></router-link>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import global from "@/composables/global";
import axios from "axios";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

@Options({
  components: {
    Loading,
  }
})
export default class App extends Vue {
  isLoading:Boolean = false;
  refCount:number = 0;

  created() {
      let { setLoading } = global;
      axios.interceptors.request.use((config) => {
        setLoading(true);
        return config;
      }, (error) => {
        setLoading(false);
        return Promise.reject(error);
      });

      axios.interceptors.response.use((response) => {
        setLoading(false);
        return response;
      }, (error) => {
        setLoading(false);
        return Promise.reject(error);
      });
    }

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
}
</script>
