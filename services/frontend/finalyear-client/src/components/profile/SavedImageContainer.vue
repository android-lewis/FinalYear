<template>
    <div>
        <img :src="thumbnail" class="object-cover w-full h-auto" alt="Thumbnail Image"/>
    </div>
    <div>
        <p>{{ title }}</p>
    </div>
</template>
<script lang="ts">
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
        return { thumbnail, title }
    }
})
</script>