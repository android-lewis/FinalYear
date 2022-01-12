import { reactive, readonly } from "vue";

const state = reactive({
    register: false,
    uploadImageURL: "",
    genImageURL: ""
});

const setGenImageURL = function(url:string){
    state.genImageURL = url;
}

const setUploadImageURL = function(url:string) {
    state.uploadImageURL = url;
}

const flip_register = function() {
    state.register = !state.register;
};

export default { state: readonly(state), flip_register, setUploadImageURL, setGenImageURL };