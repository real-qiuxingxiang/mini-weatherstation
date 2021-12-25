<template>
    <div id="index">
        <NavigationBar :isIndexActive="true" :running="running" @running_status_changed="running_status_changed"/>
        <RealTimeData :running="running"/>
    </div>
</template>

<script>
    import NavigationBar from '../components/NavigationBar.vue'
    import RealTimeData from '../components/RealTimeData.vue'
    import axios from "axios";

    export default {
        name: 'IndexApp',
        components: {
            NavigationBar,
            RealTimeData
        },
        data () {
            return {
                running: null
            }
        },
        methods: {
            running_status_changed (msg){
                this.running = msg
            }
        },
        created () {
            axios
                .get('https://Your IP/api/isRunning.php')
                .then(response => (this.running = Number(response["data"][0]["running"])))
                .catch(function (error) { // 请求失败处理
                    console.log(error);
                });
        }
    }
</script>

