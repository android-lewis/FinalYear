<template>
  <div class="overflow-hidden w-full h-screen grid grid-cols-3">
    <LoginComponent v-if="reg" class="self-center col-span-1 sm:col-span-3"/>
    <Register v-else class="self-center col-span-3 sm:col-span-1"/>
    <div class="bg-cover hidden sm:col-span-3" :style="{backgroundImage: 'url(' + bgSplash + ')'}" />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import LoginComponent from "@/components/Login.vue"; // @ is an alias to /src
import Register from "@/components/Register.vue";
import global from "../composables/global.ts";

@Options({
  components: {
    LoginComponent,
    Register
  },
})
export default class Login extends Vue {

  get reg(){
    const { state, flip_register } = global;
    return state.register;
  }
  get bgSplash(){
    return new URL("../assets/login-items/login-splash2x.png", import.meta.url).href;
  }
}
</script>