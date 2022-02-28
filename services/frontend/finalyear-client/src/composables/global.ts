import { reactive, readonly } from "vue";

const state = reactive({
    register: false,
    isAuth: false,
    uploadImageURL: "",
    genImageURL: "",
    showModal: false,
    isLoading: false,
    refCount: 0,
});

const setAuth = function(loggedin:boolean){
    state.isAuth = loggedin;
};

const setLoading = function(loading:boolean){
    if (loading) {
        state.refCount++;
        state.isLoading = true;
        console.log(state.isLoading);
      } else if (state.refCount > 0) {
        state.refCount--;
        state.isLoading = (state.refCount > 0);
      }
}

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

export default { state: readonly(state), flip_register, setUploadImageURL, setGenImageURL, setAuth, show_modal, setLoading };