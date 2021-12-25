import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';

import "jquery";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "echarts/lib/chart/line";
import echarts from "echarts";
import axios from "axios";

import Index from "./pages/index";
import DataList from "./pages/datalist";
import Chart from "./pages/chart";
import Login from "./pages/login";

Vue.prototype.$echarts = echarts; //将echarts注册成Vue的全局属性
Vue.config.productionTip = false;
Vue.use(VueRouter);


const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: Index,
            meta: {
                login_required: true,
                title: '速览 - 小型自动气象站'
            }
        },
        {
            path: '/login',
            component: Login,
            meta: {
                login_required: false,
                title: '登录 - 小型自动气象站'
            }
        },
        {
            path: '/datalist',
            component: DataList,
            meta: {
                login_required: true,
                title: '数据列表 - 小型自动气象站'
            }
        },
        {
            path: '/chart',
            component: Chart,
            meta: {
                login_required: true,
                title: '图表 - 小型自动气象站'
            }
        },
        {
            path: "*",
            redirect: "/"
        }
    ]
});

router.beforeEach((to, from, next) => {
    if(to.meta.login_required){
        axios
            .get("https://Your IP/api/isLogin.php?token=" + localStorage.getItem('Q_token'))
            .then((response) => {
                console.log(response["data"])
                if(!response["data"]){
                    if (to.meta.title) {
                        document.title = to.meta.title;
                    }
                    next('/login')
                    alert("登录已过期，请登录")
                }
            })
            .catch(function (error) { // 请求失败处理
                console.log(error);
            });
    }

    /* 路由发生变化修改页面title */
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    next();
});

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
