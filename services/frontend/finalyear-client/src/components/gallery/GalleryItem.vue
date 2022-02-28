<template>
    <div>
        <div id="image-container"><img :src="imgSrc" class="object-cover w-full h-auto" alt="gallery image"></div>
        <div id="details-container"><p>{{galleryName}}</p><button><img v-if="liked" src="../assets/gallery-items/filled-heart.svg" /><img v-else src="../assets/gallery-items/unfilled-heart.svg" /></button></div>
    </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

export default class ImageContainer extends Vue {
    @Prop()
    imgSrc!: string;
    @Prop()
    galleryName!: string;
    @Prop()
    galleryId!: string;
    @Prop()
    imageId!: string;
    @Prop({ default: false })
    liked!: Boolean;

}

</script>