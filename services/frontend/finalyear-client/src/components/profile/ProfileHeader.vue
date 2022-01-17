<template>
  <div class="container p-5 mx-auto mt-5 bg-gray-200 grid sm:grid-cols-6 gap-4">
    <div ref="profileImage" class="hidden p-10 w-full h-auto col-span-2 sm:block">
        <img src="https://randomuser.me/api/portraits/men/48.jpg" class="rounded-full border border-gray-100 w-full h-auto" alt="profile image"/>
    </div>
    <div ref="detailsContainer" class="col-span-3 flex flex-col px-5 py-10 gap-6">
        <p class="text-6xl font-body font-bold">Lewis Baston</p>
        <p class="text-2xl font-body font-medium">Job Title</p>
        <p class="text-lg font-body">Bio testing lorum ipsum...</p>
    </div>
    <div class="col-span-1 grid grid-rows-2 grid-flow-col justify-end p-5">
        <div>Icon</div>
        <div></div>
    </div>
  </div>
</template>
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import axios from "axios";
import global from "../composables/global";

@Options({})
export default class ProfileHeader extends Vue {
}
</script>