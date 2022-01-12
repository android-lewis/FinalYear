<template>
  <nav class="sticky top-0 w-screen max-h-100 flex justify-around mx-auto bg-zinc-900">
    <div class="items-center flex flex-row flex-nowrap">
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/gallery" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/image-nav.svg" alt="Image Icon for Gallery Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/camera-nav.svg" alt="Camera Icon for Home Page"/></router-link></div>
      <div class="h-full p-6 hover:bg-zinc-600 transition duration-500"><router-link to="/login" class="text-orange-600 text-lg font-body font-medium"><img src="./assets/nav-items/user-nav.svg" alt="Image Icon for Gallery Page"/></router-link></div>
    </div>
  </nav>
  <router-view />
</template>
