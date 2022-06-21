import Vue from "vue";
import VueRouter from "vue-router";
import login from "../views/login.vue"
import main from "../views/main.vue"
import userConfig from "../views/userConfig.vue"
import electriConfig from "../views/electriConfig.vue"
import waterConfig from "../views/waterConfig.vue"
import dataShow from "../views/dataShow.vue"
import propertyConfig from "../views/propertyConfig.vue"
import pakingConfig from "../views/pakingConfig.vue"
import csConfig from "../views/csConfig.vue"
Vue.use(VueRouter);

const routes = [
		{
			path:"/",
			redirect:"/login"
		},
		{
			  path: "/login",
			  name: "login",
			  component:login
		},
		{
			  path: "/main",
			  name: "main",
			  component:main,
			  redirect:"/main/dataShow",
			  children:[
				{
				  path: "userConfig",
				  name: "userConfig",
				  component:userConfig,
				},
				{
				  path: "electriConfig",
				  name: "electriConfig",
				  component:electriConfig,
				},
				{
				  path: "waterConfig",
				  name: "waterConfig",
				  component:waterConfig,
				},
				{
				  path: "dataShow",
				  name: "dataShow",
				  component:dataShow,
				},
				{
				  path: "propertyConfig",
				  name: "propertyConfig",
				  component:propertyConfig,
				},
				{
				  path: "pakingConfig",
				  name: "pakingConfig",
				  component:pakingConfig,
				},
				{
				  path: "csConfig",
				  name: "csConfig",
				  component:csConfig,
				},
			  ]
		},
];

const router = new VueRouter({
  routes,
  mode:'history'
});

export default router;
