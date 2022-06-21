import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Vant from 'vant';
import Axios from "axios"
import 'vant/lib/index.css';
import { Toast } from 'vant';
import { Tab, Tabs } from 'vant';
import { PullRefresh } from 'vant';
import md5 from "js-md5";
Vue.use(Tab);
Vue.use(Tabs);
Vue.use(Vant);
Vue.use(Toast);
Vue.use(PullRefresh);
Vue.prototype.$axios=Axios;
Vue.prototype.url="http://127.0.0.1:8000";
Vue.prototype.$md5=md5;
Vue.config.productionTip = false;
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
