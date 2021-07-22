import Vue from 'vue'
import App from './App.vue'
import UserPage from './components/UserPage.vue'
import Orders from './components/Orders.vue'
import CreateOrder from './components/CreateOrder.vue'
import Main from './components/Main.vue'
import Autho from './components/Autho.vue'
import Catalog from './components/Catalog.vue'
import Reg from './components/Reg.vue'
import Plug from './components/plug.vue'
import Basket from './components/Basket.vue'
import CustomerData from '@/components/CustomerData.vue'
import Tracking from "@/components/Tracking.vue";
import Settings from "@/components/Settings.vue";
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import YmapPlugin from 'vue-yandex-maps'
import PaymentOrderLoad from "@/components/PaymentOrderLoad.vue";

Vue.use(VueResource)
Vue.config.productionTip = false
Vue.use(VueRouter)

const settings = {
	apiKey: '07470f42-pnc422-40e8-b6b2-0d20f1866092',
	lang: 'ru_RU',
	coordorder: 'latlong',
	version: '2.1'
}

Vue.use(YmapPlugin, settings)


const router=new VueRouter({
	mode:'history',
	routes:[
		{path:'/userPage',component:UserPage},
		{path:'/orders',component:Orders},
		{path:'/create',component:CreateOrder},
		{path:'/reg',component:Reg},
		{path:'/autho',component:Autho},
		{path:'/',component:Main},
		{path:'/plug',component:Plug},
		{path:'/basket',component:Basket},
		{path:'/custdata',component:CustomerData},
		{path:'/catalog',component:Catalog},
		{path:'/tracking',component:Tracking},
		{path:'/settings',component:Settings},
		{path:'/paymentLoad',component:PaymentOrderLoad}
	],
	linkActiveClass:'active'
})

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
