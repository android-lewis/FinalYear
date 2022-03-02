<template>
    <div class="max-w-sm bg-white rounded-lg border border-gray-200 shadow-md col-span-1">
    <a v-on:click="navigate">
        <img class="rounded-t-lg" :src="thumbnail" alt="thumbnail" />
    </a>
    <div class="p-5">
        <a v-on:click="navigate">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">{{title}}</h5>
        </a>
    </div>
</div>
</template>
<script lang="ts">
import router from "@/router";
import { defineComponent } from "vue";

export default defineComponent({
    name: "SavedImageContainer",
    props: {
        thumbnail: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        }
    },
    setup(props:any) {
        const thumbnail = props.thumbnail;
        const title = props.title;

        const navigate = () => {
            router.push(`/gallery/${title}`)
        }
        return { thumbnail, title, navigate }
    }
})
</script>