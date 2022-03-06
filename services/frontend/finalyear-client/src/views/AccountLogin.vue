<template>
  <Account v-if="auth" />
  <Login v-else/>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import global from "@/composables/global";
import Login from "@/views/Login.vue";
import Account from "@/views/Account.vue";

@Options({
  components: {
    Login,
    Account
  },
})
export default class AccountLogin extends Vue {
  auth: Boolean = sessionStorage.getItem('token') != undefined ? true : false;
}
</script>