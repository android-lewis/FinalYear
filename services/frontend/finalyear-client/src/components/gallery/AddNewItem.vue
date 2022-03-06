<template>
    <div class="max-w-sm bg-white border border-gray-200 shadow-md col-span-1">
        <div class="p-[50%]">
            <img class="w-full" src="@/assets/gallery-items/plus.svg" alt="thumbnail" />
        </div>
    </div>
</template>
<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";

export default defineComponent({
    name: "AddNewItem",
    setup(props:any) {
    }
})
</script>