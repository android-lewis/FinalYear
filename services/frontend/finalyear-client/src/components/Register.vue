<template>
    <div class="bg-white px-10 pt-6 pb-8 mb-4 flex flex-col">
        <div class="mb-4">
            <label class="block text-grey-darker text-sm font-bold mb-2" for="fname">
                First Name
            </label>
            <input ref="fname" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker" id="fname" type="text" placeholder="First Name">
        </div>
        <div class="mb-4">
            <label class="block text-grey-darker text-sm font-bold mb-2" for="lname">
                Last Name
            </label>
            <input ref="lname" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker" id="lname" type="text" placeholder="Last Name">
        </div>
        <div class="mb-4">
            <label class="block text-grey-darker text-sm font-bold mb-2" for="email">
                Email
            </label>
            <input ref="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker" id="regEmail" type="email" placeholder="Email">
        </div>
        <div class="mb-6">
            <label class="block text-grey-darker text-sm font-bold mb-2" for="regPassword">
                Password
            </label>
            <input ref="password" class="shadow appearance-none border border-red rounded w-full py-2 px-3 text-grey-darker mb-3" id="regPassword" type="password" placeholder="******************">
            <p class="text-red-500 text-xs italic">Please choose a password.</p>
        </div>
        <div class="flex flex-col items-center justify-between gap-5">
            <button v-on:click="handleRegister" class="w-full bg-orange-600 hover:bg-orange-400 text-white font-bold font-body py-4 px-4" type="button">
                Sign Up
            </button>
            <button v-on:click="registerLoad" class="w-full bg-gray-600 hover:bg-gray-400 text-white font-bold font-body py-4 px-4" type="button">
                Sign In
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import global from "../composables/global";
import axios from "axios";
import router from "@/router";

@Options({})

export default class Register extends Vue {
  $refs!: {
    fname: HTMLInputElement,
    lname: HTMLInputElement, 
    email: HTMLInputElement,
    password: HTMLInputElement
  }

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

  handleRegister() {
    console.log("Handling");

    const postData = {
        f_name: this.$refs.fname.value,
        l_name: this.$refs.lname.value,
        email: this.$refs.email.value,
        password: this.$refs.password.value
    }
    
    console.log(postData);

    axios.post('/api/user/register',
        postData,
        {
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        console.log(response.data);
        router.replace('/account');
    })
    .catch(function(){
        console.log('FAILURE!!');
    })

  }
}
</script>
