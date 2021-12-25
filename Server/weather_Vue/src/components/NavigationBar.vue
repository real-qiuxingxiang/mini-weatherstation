<template>
    <div id="NavigationBar">
        <nav class="navbar navbar-expand-md navbar-dark bg-dark">
            <a class="navbar-brand" href="/">小型自动气象站 控制台</a>

            <!-- 展开/收起导航栏按钮 -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="collapsibleNavbar">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item" v-bind:class="{ active: isIndexActive }">
                        <router-link class="nav-link" to="/">速览</router-link>
                    </li>
                    <li class="nav-item" v-bind:class="{ active: isDataListActive }">
                        <router-link class="nav-link" to="/datalist">数据列表</router-link>
                    </li>
                    <li class="nav-item" v-bind:class="{ active: isChartActive }">
                        <router-link class="nav-link" to="/chart">图表</router-link>
                    </li>
                </ul>
                <div class="btn-group">
                    <template v-if="running">
                        <button type="button" class="btn btn-success" data-toggle="modal" data-target="#Start" disabled>启动</button>
                        <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Stop">关闭</button>
                    </template>
                    <template v-else>
                        <button type="button" class="btn btn-success" data-toggle="modal" data-target="#Start">启动</button>
                        <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Stop" disabled>关闭</button>
                    </template>
                </div>
                <button class="btn btn-outline-success m-2 my-2 my-sm-0" type="submit" v-on:click="logout" >登出</button>
            </div>
            <div class="modal fade" id="Start">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <!-- 模态框头部 -->
                        <div class="modal-header">
                            <h4 class="modal-title">确认</h4>
                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                        </div>
                        <!-- 模态框主体 -->
                        <div class="modal-body">
                            是否启动气象站？
                        </div>
                        <!-- 模态框底部 -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" data-dismiss="modal" v-on:click="start">确定</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal fade" id="Stop">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <!-- 模态框头部 -->
                        <div class="modal-header">
                            <h4 class="modal-title">确认</h4>
                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                        </div>
                        <!-- 模态框主体 -->
                        <div class="modal-body">
                            是否关闭气象站？
                        </div>
                        <!-- 模态框底部 -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" data-dismiss="modal" v-on:click="stop">确定</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <template v-if="show_time">
            <div class="container">
                <h1></h1>
                <div class="row" >
                    <div class="col" >
                        <div class="alert alert-success fade show">
                            <strong>成功!</strong> {{ show_message }}
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
    import mqtt from "mqtt";

    export default {
        name: 'NavigationBar',
        data () {
            return {
                show_message: null,
                show_time: 0,
                show_timer: 0,
            }
        },
        props: {
            running: Number,
            isIndexActive: {
                default() {
                    return false;
                }
            },
            isDataListActive: {
                default() {
                    return false;
                }
            },
            isChartActive: {
                default() {
                    return false;
                }
            }
        },
        created () {

        },
        methods: {
            countDown: function () {
                clearInterval(this.show_timer)
                this.show_time = 3
                this.show_timer = setInterval(()=>{
                    this.show_time -= 1
                    if(this.show_time === 0){
                        clearInterval(this.show_timer)
                    }
                },1000)
            },
            start: function () {
                //this.running = 1
                this.$emit("running_status_changed", 1)
                this.show_message = "气象站已启动。"
                var client = mqtt.connect('ws://176.122.151.119:8083/mqtt') // you add a ws:// url here
                client.publish("/control", "1")
                console.log("已发送：1")
                this.countDown()
            },
            stop: function () {
                //this.running = 0
                this.$emit("running_status_changed", 0)
                this.show_message = "气象站已关闭。"
                var client = mqtt.connect('ws://176.122.151.119:8083/mqtt') // you add a ws:// url here
                client.publish("/control", "0")
                console.log("已发送：0")
                this.countDown()
            },
            logout: function () {
                localStorage.clear()
                this.$router.push('/login')
            }
        },
        destroy() {
            clearInterval(this.show_timer);
        }
    }
</script>