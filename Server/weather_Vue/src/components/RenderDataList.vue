<template>
    <div id="DataList">
        <template v-if="apply_show_time">
            <div class="container">
                <h1></h1>
                <div class="row" >
                    <div class="col" >
                        <div class="alert alert-danger fade show">
                            <strong>失败!</strong> {{ show_message }}
                        </div>
                    </div>
                </div>
            </div>
        </template>
        <h1></h1>
        <div class="container">
            <div class="row" >
                <div class="col" >
                    <div class="card">
                        <div class="card-header bg-dark text-white">筛选</div>
                        <div class="card-body">
                            <div class="row" >
                                <div class="col-sm-6" >
                                    <label>时间范围：</label>
                                    <input type="date" value="" id="from_date" v-model="from_date"/> to <input type="date" value="" id="to_date" v-model="to_date"/>
                                </div>
                                <div class="col-sm-5" >
                                    <label>时间排序：</label>
                                    <label><input type="radio" v-model="order" value="increase">升序</label>
                                    <label><input type="radio" v-model="order" value="decrease">降序</label>
                                </div>
                                <div class="col-sm-1" >
                                    <button type="button" class="btn btn-primary" v-on:click="apply">应用</button>
                                </div>
                            </div>
                            <div class="row" >
                                <div class="col-sm-2" >
                                    <label>温度范围：</label>
                                    <input v-model="from_temperature" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/> to <input v-model="to_temperature" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/>
                                </div>
                                <div class="col-sm-2" >
                                    <label>湿度范围：</label>
                                    <input v-model="from_humidity" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/> to <input v-model="to_humidity" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/>
                                </div>
                                <div class="col-sm-2" >
                                    <label>气压范围：</label>
                                    <input v-model="from_pressure" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/> to <input v-model="to_pressure" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/>
                                </div>
                                <div class="col-sm-2" >
                                    <label>风速范围：</label>
                                    <input v-model="from_wind_speed" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/> to <input v-model="to_wind_speed" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/>
                                </div>
                                <div class="col-sm-2" >
                                    <label>风向范围：</label>
                                    <input v-model="from_wind_direction" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/> to <input v-model="to_wind_direction" value="" type="number" οnkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <h1> </h1>
            <div class="row" >
                <div class="col" >
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
            <div class="row" >
                <div class="btn-group m-auto">
                    <template v-if="offset == 0">
                        <button type="button" class="btn-light" disabled>上一页</button>
                        <button type="button" class="btn-light" disabled>{{ page }}</button>
                        <button type="button" class="btn-light" v-on:click="nextPage">下一页</button>
                    </template>
                    <template v-else>
                        <button type="button" class="btn-light" v-on:click="previousPage">上一页</button>
                        <button type="button" class="btn-light" disabled>{{ page }}</button>
                        <button type="button" class="btn-light" v-on:click="nextPage">下一页</button>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'DataList',
        data () {
            return {
                dataset: null,
                page: 1,
                offset: 0,
                apply_show_time: 0,
                show_timer: 0,
                from_date: '',
                to_date: '',
                order: 'decrease',
                show_message: '',
                from_temperature: '',
                to_temperature: '',
                from_humidity: '',
                to_humidity: '',
                from_pressure: '',
                to_pressure: '',
                from_wind_speed: '',
                to_wind_speed: '',
                from_wind_direction: '',
                to_wind_direction: '',
            }
        },
        created () {
            axios
                .get('https://Your IP/api/listData.php?offset=' + this.offset)
                .then(response => (this.dataset = response["data"]))
                .catch(function (error) { // 请求失败处理
                    console.log(error);
                });
        },
        methods: {
            applyCountDown: function () {
                clearInterval(this.show_timer)
                this.apply_show_time = 3
                this.show_timer = setInterval(()=>{
                    this.apply_show_time -= 1
                    if(this.apply_show_time === 0){
                        clearInterval(this.show_timer)
                    }
                },1000)
            },
            apply: function () {
                if((this.from_date === "" && this.to_date === "") || (this.from_date !== "" && this.to_date !== "")){
                    this.offset = 0
                    this.page = 1
                    axios
                        .get('https://Your IP/api/listData.php?offset=' + this.offset
                            + "&from_date=" + this.from_date
                            + "&to_date=" + this.to_date
                            + "&order=" + this.order
                            + "&from_temperature=" + this.from_temperature
                            + "&to_temperature=" + this.to_temperature
                            + "&from_humidity=" + this.from_humidity
                            + "&to_humidity=" + this.to_humidity
                            + "&from_pressure=" + this.from_pressure
                            + "&to_pressure=" + this.to_pressure
                            + "&from_wind_speed=" + this.from_wind_speed
                            + "&to_wind_speed=" + this.to_wind_speed
                            + "&from_wind_direction=" + this.from_wind_direction
                            + "&to_wind_direction=" + this.to_wind_direction
                        )
                        .then(response => (this.dataset = response["data"]))
                        .catch(function (error) { // 请求失败处理
                            console.log(error);
                        });
                }else {
                    this.show_message = "请选择开始时间或结束时间！"
                    this.applyCountDown()
                }
            },
            previousPage: function () {
                if (this.offset > 0){
                    this.offset -= 10
                    this.page -= 1
                    axios
                        .get('https://Your IP/api/listData.php?offset=' + this.offset
                            + "&from_date=" + this.from_date
                            + "&to_date=" + this.to_date
                            + "&order=" + this.order
                            + "&from_temperature=" + this.from_temperature
                            + "&to_temperature=" + this.to_temperature
                            + "&from_humidity=" + this.from_humidity
                            + "&to_humidity=" + this.to_humidity
                            + "&from_pressure=" + this.from_pressure
                            + "&to_pressure=" + this.to_pressure
                            + "&from_wind_speed=" + this.from_wind_speed
                            + "&to_wind_speed=" + this.to_wind_speed
                            + "&from_wind_direction=" + this.from_wind_direction
                            + "&to_wind_direction=" + this.to_wind_direction
                        )
                        .then(response => (this.dataset = response["data"]))
                        .catch(function (error) { // 请求失败处理
                            console.log(error);
                        });
                }
            },
            nextPage: function () {
                this.offset += 10
                this.page += 1
                axios
                    .get('https://Your IP/api/listData.php?offset=' + this.offset
                        + "&from_date=" + this.from_date
                        + "&to_date=" + this.to_date
                        + "&order=" + this.order
                        + "&from_temperature=" + this.from_temperature
                        + "&to_temperature=" + this.to_temperature
                        + "&from_humidity=" + this.from_humidity
                        + "&to_humidity=" + this.to_humidity
                        + "&from_pressure=" + this.from_pressure
                        + "&to_pressure=" + this.to_pressure
                        + "&from_wind_speed=" + this.from_wind_speed
                        + "&to_wind_speed=" + this.to_wind_speed
                        + "&from_wind_direction=" + this.from_wind_direction
                        + "&to_wind_direction=" + this.to_wind_direction
                    )
                    .then(response => (this.dataset = response["data"]))
                    .catch(function (error) { // 请求失败处理
                        console.log(error);
                    });
            }
        }
    }
</script>