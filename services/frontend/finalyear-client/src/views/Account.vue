<template>
  <div class="flex flex-col content-center">
    <ProfileHeader />
    <div class="container p-5 mx-auto mt-5 bg-gray-200 grid sm:grid-cols-3 gap-4">
      <SavedImageContainer thumbnail="https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" title="Uploaded" />
      <SavedImageContainer thumbnail="https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" title="Generated" />
      <SavedImageContainer thumbnail="https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" title="Combined" />
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import axios from "axios";
import global from "../composables/global";
import ProfileHeader from "@/components/profile/ProfileHeader.vue"
import SavedImageContainer from "@/components/profile/SavedImageContainer.vue";

@Options({
  components: {
    ProfileHeader,
    SavedImageContainer,
  }
})
export default class Account extends Vue {
}
</script>