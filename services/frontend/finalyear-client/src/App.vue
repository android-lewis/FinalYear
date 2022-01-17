<template>
  <nav class="sticky top-0 w-screen max-h-100 flex justify-around mx-auto bg-zinc-900">
    <div class="items-center flex flex-row flex-nowrap">
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/gallery" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/image-nav.svg" alt="Image Icon for Gallery Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/camera-nav.svg" alt="Camera Icon for Home Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500">
        <router-link v-show="!determineAuth" to="/login" class="text-orange-600 text-lg font-body font-medium">
          <img src="./assets/nav-items/user-nav.svg" alt="Profile Icon for Login Page"/>
        </router-link>
        <router-link v-show="determineAuth" to="/account" class="text-orange-600 text-lg font-body font-medium">
          <img src="./assets/nav-items/user-nav.svg" alt="Profile Icon for Account Page"/>
        </router-link>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import global from "@/composables/global";

@Options({})
export default class App extends Vue {

  public determineAuth(): Boolean {
    const { state } = global;
    return state.isAuth;
  }
}
</script>
