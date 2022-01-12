import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/account",
    name: "Account",

    component: () =>
      import("../views/Account.vue"),
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
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
