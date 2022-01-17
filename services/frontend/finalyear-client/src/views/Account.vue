<template>
  <div class="flex flex-col content-center">
    <ProfileHeader />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import axios from "axios";
import global from "../composables/global";
import ProfileHeader from "@/components/profile/ProfileHeader.vue"

@Options({
  components: {
    ProfileHeader
  }
})
export default class Account extends Vue {
}
</script>