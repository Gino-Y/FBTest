import Vue from "vue";
import VueRouter from "vue-router";
import Register from "../views/register.vue";
import Login from "../views/login.vue"
import Entrance from "../views/entrance.vue"
import Detail from "../views/detail.vue"
Vue.use(VueRouter);
const originalPush = VueRouter.prototype.push
  VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
	path:"/",
	redirect:"/login"
  },
  {
	  path: "/login",
	  name: "login",
	  component:Login
  },
  {
    path: "/register",
    name: "register",
    component:Register
  },
  {
	path:"/entrance",
	name:"entrance",
	component:Entrance
  },
  {
  	path:"/detail",
  	name:"detail",
  	component:Detail,
  }
];

const router = new VueRouter({
  routes,
  mode:'history'
});

export default router;
