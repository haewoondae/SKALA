import { createRouter, createWebHistory } from "vue-router";
import LoginMain from "./components/Router/LoginMain.vue";
import SignupMain from "./components/Router/SignupMain.vue";
import ServiceMain from "./components/Router/ServiceMain.vue";

const routes = [
  { name: "/", path: "/", component: LoginMain },
  { name: "/login", path: "/login", component: LoginMain },
  { path: "/signup", component: SignupMain },
  { path: "/service", component: ServiceMain },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;