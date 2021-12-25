<template>
  <div id="RealTimeData">
    <!-- 数据显示 -->
    <h1></h1>
    <div class="container">
      <div class="card">
        <div class="card-header bg-dark text-white">实时数据</div>
        <div class="card-body">
          <div class="row ">
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">时间</h4>
                  <h5 class="card-text">{{ time }}</h5>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">温度</h4>
                  <h5 class="card-text">{{ temperature }}</h5>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">湿度</h4>
                  <h5 class="card-text">{{ humidity }}</h5>
                </div>
              </div>
            </div>
          </div>
          <h1></h1>
          <div class="row ">
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">气压</h4>
                  <h5 class="card-text">{{ pressure }}</h5>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">风速</h4>
                  <h5 class="card-text">{{ wind_speed }}</h5>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">风向</h4>
                  <h5 class="card-text">{{ wind_direction }}</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div class="container">
      <h1> </h1>
      <div class="row" >
        <div class="col" >
          <div class="card">
            <div class="card-header bg-dark text-white">最新10条记录</div>
            <div class="card-body">
              <table class="table table-hover">
                <thead class="thead-light">
                <tr>
                  <th>时间</th>
                  <th>温度</th>
                  <th>湿度</th>
                  <th>风速</th>
                  <th>风向</th>
                  <th>气压</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="data in dataset" :key="data.id">
                  <td>{{ data.time }}</td>
                  <td>{{ data.temperature }}</td>
                  <td>{{ data.humidity }}</td>
                  <td>{{ data.wind_speed }}</td>
                  <td>{{ data.wind_direction }}</td>
                  <td>{{ data.pressure }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import mqtt from "mqtt";
  var client = mqtt.connect('ws://176.122.151.119:8083/mqtt')
  export default {
    name: 'RealTimeData',
    data () {
      return {
        time: null,
        temperature: null,
        humidity: null,
        wind_speed: null,
        wind_direction: null,
        pressure: null,
        rainfall: null,
        get_data_timer: 0,
        dataset: null,
        timer: 0,
        msg: null,
      }
    },
    props: [
      'running'
    ],
    created () {
      this.realTimeData()
      axios
          .get('https://Your IP/api/Latest.php')
          .then(response => {
            this.temperature = response["data"][0]["temperature"] + "°C"
            this.humidity = response["data"][0]["humidity"] + "%"
            this.wind_speed = response["data"][0]["wind_speed"] + "m/s"
            this.wind_direction = response["data"][0]["wind_direction"]
            this.pressure = response["data"][0]["pressure"] + "mbar"
            this.time = response["data"][0]["time"]
          })
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });
      axios
          .get('https://Your IP/api/Latest10.php')
          .then(response => (this.dataset = response["data"]))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });
    },
    methods: {
      realTimeData: function () {
        client.on('connect', function () {
          console.log('连接成功');
          client.subscribe('/weather_station', { qos: 1 }, (error) => {
            if (!error) {
              console.log('订阅成功')
            } else {
              console.log('订阅失败')
            }
          })
        });
        // 接收消息处理
        client.on('message', (topic, message) => {
          console.log(message.toString());
          let response = JSON.parse(message.toString())
          this.temperature = response["temperature"] + "°C"
          this.humidity = response["humidity"] + "%"
          this.wind_speed = response["wind_speed"] + "m/s"
          this.wind_direction = response["wind_direction"]
          this.pressure = response["pressure"] + "mbar"
          this.time = response["time"]
        });
        // 断开发起重连
        client.on('reconnect', (error) => {
          console.log('正在重连:', error)
        });
        // 链接异常处理
        client.on('error', (error) => {
          console.log('连接失败:', error)
        })
      },
      refresh: function () {
        if(this.get_data_timer){
          clearInterval(this.get_data_timer)
        }else{
          this.get_data_timer = setInterval(()=>{
            axios
                .get('https://Your IP/api/Latest10.php')
                .then(response => (this.dataset = response["data"]))
                .catch(function (error) { // 请求失败处理
                  console.log(error);
                });
          },5000)
        }
      }
    },
    watch: {
      running: function (val) {
        if (val == 1){
          this.refresh()
        }else{
          clearInterval(this.get_data_timer);
        }
      }
    },
    destroy() {
      clearInterval(this.get_data_timer);
      clearInterval(this.timer);
    }
  }
</script>
