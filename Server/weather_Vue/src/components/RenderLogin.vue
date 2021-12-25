<template>
    <div class="container">
        <div class="row row-centered">
            <div class="col-xs-6 col-md-4 col-center-block">
                <h1 class="textcolor">小型自动气象站</h1>
                <!-- 登录 -->
                 <template v-if="isLogin">
                     <!-- 输入用户名 -->
                    <div class="input-group input-group-md">
                        <span class="input-group-addon" id="sizing-addon1">
                            <i class="glyphicon glyphicon-user" aria-hidden="true"></i></span>
                        <input type="text" class="form-control" v-model="user.username" placeholder="请输入用户名"/>
                    </div>
                    <!-- 输入密码 -->
                    <div class="edit input-group input-group-md">
                        <span class="input-group-addon" id="sizing-addon2">
                            <i class="glyphicon glyphicon-lock"></i></span>
                        <input type="password" class="form-control" v-model="user.password" placeholder="请输入密码"/>
                    </div>
                    <br/>
                     <template v-if="show_time">
                        <p style="color:red">{{ show_message }}</p>
                     </template>
                    <button type="submit" class="btn btn-success btn-block" v-on:click="login">登录</button>

                    <a type="submit" class="btn btn-primary btn-block" v-on:click="isLogin = false">注册</a>

                </template>
                <!-- 注册 -->
                <template v-else>
                    <!-- 输入用户名 -->
                    <div class="edit input-group input-group-md">
                        <span class="input-group-addon">
                            <i class="glyphicon glyphicon-user"></i></span>
                        <input type="text" class="form-control" v-model="user.username" placeholder="请输入用户名"/>
                    </div>
                    <!-- 输入密码 -->
                    <div class="edit input-group input-group-md">
                        <span class="input-group-addon">
                            <i class="glyphicon glyphicon-lock"></i></span>
                        <input type="password" class="form-control" v-model="user.password" placeholder="请输入密码"/>
                    </div>
                    <!-- 确认密码 -->
                    <div class="edit input-group input-group-md">
                        <span class="input-group-addon">
                            <i class="glyphicon glyphicon-ok"></i></span>
                        <input type="password" class="form-control" v-model="confirm" placeholder="请再次确认密码"/>
                    </div>
                    <br/>
                    <template v-if="show_time">
                        <p style="color:red">{{ show_message }}</p>
                    </template>
                    <button type="Submit" class="btn btn-success btn-block" v-on:click="register">注册</button>
                    <button class="btn btn-primary btn-block" v-on:click=" isLogin = true">返回登录</button>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Login',
        data () {
            return {
                isLogin: true,
                confirm: null,
                show_message: null,
                show_time: 0,
                show_timer: 0
            }
        },
        props: {
            user: {
                type: Object,
                default() {
                    return {
                        username: "",
                        password: ""
                    };
                }

            },
            isShow: {
                type: Number,
                default() {
                    return 0
                }
            },
        },
        methods: {
            countDown: function () {
                clearInterval(this.show_timer);
                this.show_time = 3;
                this.show_timer = setInterval(()=>{
                    this.show_time -= 1;
                    if(this.show_time === 0){
                        clearInterval(this.show_timer)
                    }
                },1000);
                this.$emit("isShowReset", 0)
            },
            login: function () {
                if(this.user.username !== "" && this.user.password !== ""){
                    this.$emit("login", this.user)
                }else {
                    console.log("null")
                }
            },
            register: function () {
                if(this.user.username !== ""){
                    if(this.user.password !== "" && this.user.password === this.confirm){
                        this.$emit("register", this.user)
                    }else{
                        this.show_message = "两次输入的密码不一样！"
                        this.countDown()
                    }
                }else{
                    this.show_message = "请输入用户名！"
                    this.countDown()
                }


            }
        },
        watch: {
            isShow: {
                handler(newVal) {
                    if (newVal === 1) {
                        this.show_message = "用户名或密码错误！"
                        this.countDown()
                    }
                    if (newVal === 2) {
                        this.show_message = "数据库连接失败，请检查服务器！"
                        this.countDown()
                    }
                    if (newVal === 3) {
                        this.show_message = "注册成功！请返回登录！"
                        this.countDown()
                    }
                    if (newVal === 4) {
                        this.show_message = "用户名已存在！"
                        this.countDown()
                    }
                    if (newVal === 5) {
                        this.show_message = "数据库连接失败，请检查服务器！"
                        this.countDown()
                    }
                }
            }
        }
    }
</script>