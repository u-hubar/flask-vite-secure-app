import { registerRuntimeCompiler } from "vue";
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import Dashboard from "./views/Dashboard.vue";
import Register from "./views/Register.vue";
import Login from "./views/Login.vue";
import Logs from "./views/Logs.vue";
import NotFound from "./views/NotFound.vue";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "login",
    component: Login,
    meta: { layout: "empty" },
  },
  {
    path: "/register",
    name: "register",
    component: Register,
    meta: { layout: "empty" },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
  {
    path: "/logs",
    name: "logs",
    component: Logs,
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
