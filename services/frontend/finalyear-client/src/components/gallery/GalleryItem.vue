<template>
    <div class="max-w-sm bg-white border border-gray-200 shadow-md col-span-1">
        <img :src="thumbnail" alt="thumbnail" />
        <div class="p-5 grid grid-cols-2">
            <h5 class="mb-2 text-md font-bold tracking-tight text-gray-900 col-span-1">{{title}}</h5>
            <div class="col-span-1 flex justify-end">
                <!--<a v-if="type" v-on:click="addGallery" class="text-orange-600 text-md font-body font-medium"><img src="../../assets/gallery-items/plus.svg" alt="Add to Gallery Image"/></a>-->
                <a v-on:click="deleteImage" class="text-orange-600 text-md font-body font-medium"><img src="../../assets/gallery-items/delete.svg" alt="Delete Image"/></a>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";

export default defineComponent({
    name: "SavedImageContainer",
    emits: ['refresh', 'removeGallery'],
    props: {
        thumbnail: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        id: {
            type: String,
            required: true,
        },
        type: {
            type: Boolean,
            required: true,
        }
    },
    setup(props:any, { emit }) {
        const thumbnail = props.thumbnail;
        const title = props.title;
        const id = props.id;
        const type = props.type;
        const deleteImage = () => {
            if(type){
                axios.delete(`/api/image/delete?imageid=${id}`, { headers : { "x-access-tokens": `${sessionStorage.getItem('token')}` }}).then((response) => { console.log(response) }).catch((response) => { console.log(response)});
                emit('refresh', true);
            } else {
                emit('removeGallery', id);
            }
        }

        return { thumbnail, title, type, deleteImage }
    }
})
</script>