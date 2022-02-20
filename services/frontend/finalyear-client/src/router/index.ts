import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import AccountLogin from "../views/AccountLogin.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/account",
    name: "Account",
    component: AccountLogin,
  },
  {
    path: "/login",
    name: "Login",

    component: () =>
      import("../views/Login.vue"),
  },
  {
    path: "/gallery",
    name: "Gallery",

    component: () => 
      import("../views/Gallery.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
