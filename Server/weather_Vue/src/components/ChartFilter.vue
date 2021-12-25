<template>
    <div id="ChartFilter">
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
                                    <input type="date" value="" id="from_date" v-model="filter_option.from_date"/> to <input type="date" value="" id="to_date" v-model="filter_option.to_date"/>
                                </div>
                                <div class="col-sm-5" >
                                    <label>时间排序：</label>
                                    <label><input type="radio" v-model="filter_option.order" value="increase">升序</label>
                                    <label><input type="radio" v-model="filter_option.order" value="decrease">降序</label>
                                    <br>
                                    <label>数据：</label>
                                    <label><input type="checkbox"  v-model="checkedData" value="temperature">温度</label>
                                    <label><input type="checkbox" v-model="checkedData" value="humidity">湿度</label>
                                    <label><input type="checkbox" v-model="checkedData" value="pressure">气压</label>
                                    <label><input type="checkbox" v-model="checkedData" value="wind_speed">风速</label>
                                    <label><input type="checkbox" v-model="checkedData" value="wind_direction">风向</label>
                                </div>
                                <div class="col-sm-1" >
                                    <button type="button" class="btn btn-primary" v-on:click="apply">应用</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ChartFilterApp',
        data () {
            return {
                dataset: null,
                apply_show_time: 0,
                show_timer: 0,
                show_message: '',
                checkedData: ["temperature"],
            }
        },
        props: {
            filter_option: {
                checkedData: Array,
                page: 1,
                offset: 0,
                from_date: '',
                to_date: '',
                order: 'decrease',
            }
        },
        created () {

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
                if((this.filter_option.from_date === "" && this.filter_option.to_date === "") || (this.filter_option.from_date !== "" && this.filter_option.to_date !== "")){
                    this.filter_option.offset = 0
                    this.filter_option.page = 1
                    this.filter_option.checkedData = this.checkedData
                    this.$emit("filter_option_changed", this.filter_option)
                }else {
                    this.show_message = "请选择开始时间或结束时间！"
                    this.applyCountDown()
                }
            }
        }
    }
</script>