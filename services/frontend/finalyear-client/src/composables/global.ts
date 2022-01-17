import { reactive, readonly } from "vue";

const state = reactive({
    register: false,
    isAuth: false,
    uploadImageURL: "",
    genImageURL: "",
    showModal: false,
});

const setAuth = function(){
    state.isAuth = !state.isAuth;
};

const setGenImageURL = function(url:string){
    state.genImageURL = url;
};

const setUploadImageURL = function(url:string) {
    state.uploadImageURL = url;
};

const flip_register = function() {
    state.register = !state.register;
};

const show_modal = function(){
    state.showModal = !state.showModal;
}

export default { state: readonly(state), flip_register, setUploadImageURL, setGenImageURL, setAuth, show_modal };