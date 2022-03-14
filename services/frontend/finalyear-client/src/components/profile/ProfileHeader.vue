<template>
  <div class="container p-5 mx-auto mt-5 bg-gray-200 grid sm:grid-cols-6 gap-4">
    <div class="hidden p-10 w-full h-auto col-span-2 sm:block">
        <img ref="profileImage" src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png" class="rounded-full border border-gray-100 w-full h-auto" alt="profile image"/>
    </div>
    <div ref="detailsContainer" class="col-span-3 flex flex-col px-5 py-10 gap-6">
        <p ref="name" class="text-6xl font-body font-bold"></p>
        <p ref="bio" class="text-lg font-body">Say something about yourself...</p>
    </div>
    <div class="col-span-1 grid grid-rows-2 grid-flow-col justify-end p-5">
        <div class="grid grid-cols-2 gap-4"><div>Edit Icon</div><button v-on:click="logOut">Log out</button></div>
        <div></div>
    </div>
  </div>
</template>
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import axios from "axios";
import global from "../../composables/global";
import router from "@/router";

@Options({})
export default class ProfileHeader extends Vue {
  $refs!: {
    profileImage: HTMLImageElement
    name: HTMLElement
    title: HTMLElement
    bio: HTMLElement
    profileImageInput: HTMLInputElement
    nameInput: HTMLInputElement
    titleInput: HTMLInputElement
    bioInput: HTMLInputElement
  };

  mounted(){
    axios.get('/api/user/get', {
      headers: {
        'x-access-tokens': `${sessionStorage.getItem('token')}`
      }
    }).then((response) => {
      console.log(response);
      this.bindData(response);
    }).catch((response) => {
      console.log("FAILURE")
    })
  }

  bindData(response:any){
    let data = response.data.value;
    this.$refs.name.innerText = data.fName + " " + data.lName;
    if (data.bio != null) { this.$refs.bio.innerText = data.bio }
    if (data.profile_image != null) { this.$refs.profileImage.src = data.profile_image }
  }

  logOut() {
    const {setAuth} = global;
    setAuth(false);
    sessionStorage.removeItem('token');
    router.replace("/");
  }
}
</script>