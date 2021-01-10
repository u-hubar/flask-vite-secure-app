import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import Dashboard from "./views/Dashboard.vue";
import Login from "./views/Login.vue";
import NotFound from "./views/NotFound.vue";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Login",
    component: Login,
    meta: { layout: "empty" },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: NotFound
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;
