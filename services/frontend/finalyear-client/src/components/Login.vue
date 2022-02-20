<template>
    <div class="bg-white px-10 pt-6 pb-8 mb-4 flex flex-col gap-10">
    <div>
      <div class="mb-4">
        <label class="block text-grey-darker text-sm font-bold mb-2" for="email">
          Email
        </label>
        <input ref="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker" id="email" type="email" placeholder="Email">
      </div>
      <div class="mb-6">
        <label class="block text-grey-darker text-sm font-bold mb-2" for="password">
          Password
        </label>
        <input ref="password" v-on:change="changePass" :class="{'border-red-600' : passEmpty}" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker mb-3" id="password" type="password" placeholder="******************">
        <p v-if="passEmpty" class="text-red text-xs italic">Please enter a password.</p>
      </div>
    </div>
    <div class="flex flex-col items-center justify-between gap-5">
      <button v-on:click="handleLogin" class="bg-gray-600 hover:bg-gray-400 text-white w-full font-bold font-body py-4 px-4" type="button">
        Sign In
      </button>
      <button v-on:click="registerLoad" class="bg-orange-600 hover:bg-orange-400 text-white w-full font-bold font-body py-4 px-4" type="button">
        Sign Up
      </button>
      <a class="inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker font-body" href="#">
        Forgot Password?
      </a>
    </div>
</div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import global from "../composables/global";
import axios from "axios";
import router from "@/router";

@Options({})

export default class LoginComponent extends Vue {
  $refs!: {
    email: HTMLInputElement
    password: HTMLInputElement
  };

  passEmpty: boolean = true;

  changePass(){
    console.log(this.$refs.password.value);
    if(this.$refs.password.value === "") this.passEmpty = true;
    else this.passEmpty = false;
  }

  registerLoad() {
    const { state, flip_register } = global;
    console.log(state)
    flip_register();
    console.log(state)
  }

  handleLogin() {
    const { setAuth } = global;
    const postData = {
        email: this.$refs.email.value,
        password: this.$refs.password.value
    }
    
    axios.post('/api/user/login',
    postData,
    {
    headers: {
        'Content-Type': 'application/json'
    }
    }).then(function(response) {
        console.log(response.data);
        sessionStorage.setItem('token', response.data.token);
        setAuth(true);
        router.push("/");
    })
    .catch(function(){
        console.log('FAILURE!!');
    })

  }
}
</script>
