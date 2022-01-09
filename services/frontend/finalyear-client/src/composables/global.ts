import { reactive, readonly } from "vue";

const state = reactive({
    register: false
});

const flip_register = function() {
    state.register = !state.register;
};

export default { state: readonly(state), flip_register };