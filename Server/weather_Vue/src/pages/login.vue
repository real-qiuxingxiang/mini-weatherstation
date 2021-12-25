<template>
    <div id="app">
        <RenderLogin :isShow="isShow" @login="login" @register="register" @isShowReset="isShowReset"/>
    </div>
</template>

<style>
    .col-center-block {
      float: none;
      display: block;
      margin-left: auto;
      margin-right: auto;
      margin-top: 20%;
      text-align: center;
      max-width: 333px;
    }
    .edit {
        margin-top: 10px;
    }
</style>

<script>
    import RenderLogin from '../components/RenderLogin.vue'
    import axios from "axios";

    export default {
        name: 'LoginApp',
        components: {
            RenderLogin
        },
        data () {
            return {
                isShow: 0
            }
        },
        methods: {
            login: function (msg) {
                let username = msg.username
                let password = msg.password
                axios
                    .get("https://Your IP/api/login.php?username=" + username + "&password=" + password)
                    .then((response) => {
                        if(response["data"]["status"] === "success"){
                            localStorage.setItem('Q_token', response["data"]["token"])
                            location.href="/";
                        }
                        if(response["data"]["status"] === "db_failed"){
                            this.isShow = 2
                        }
                        if(response["data"]["status"] === "failed"){
                            this.isShow = 1
                        }
                    })
                    .catch(function (error) { // 请求失败处理
                        console.log(error);
                    });
            },
            register: function (msg) {
                let username = msg.username
                let password = msg.password
                axios
                    .get("https://Your IP/api/register.php?username=" + username + "&password=" + password)
                    .then((response) => {
                        console.log(response["data"])
                        if(response["data"] === "success"){
                            this.isShow = 3;
                        }
                        if(response["data"] === "existed"){
                            this.isShow = 4
                        }
                        if(response["data"] === "failed"){
                            this.isShow = 5
                        }
                    })
                    .catch(function (error) { // 请求失败处理
                        console.log(error);
                    });
            },
            isShowReset: function (msg) {
                this.isShow = msg
            }
        }
    }
</script>
