<template>
    <div class="container">
        <h1></h1>
        <div class="row" >
            <div class="col" >
                <div class="card">
                    <div class="card-header bg-dark text-white">Chart</div>
                    <div class="card-body">
                        <div :id="id" :style="style"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        name: "RenderChart",
        data() {
            return {
                //echarts实例
                chart: ""
            };
        },
        props: {
            //父组件需要传递的参数：id，width，height，option
            id: {
                type: String
            },
            width: {
                type: String,
                default: "100%"
            },
            height: {
                type: String,
                default: "600px"
            },
            option: {
                type: Object,
                default() {
                    return {
                        title: {
                            text: ""
                        },
                        legend: {
                            data: []
                        },
                        xAxis: {
                            data: []
                        },
                        yAxis: [
                            {
                                type: "value"
                            }
                        ],
                        series: []
                    };
                }
            }
        },
        computed: {
            style() {
                return {
                    height: this.height,
                    width: this.width
                };
            }
        },
        mounted() {
            this.init();
        },
        methods: {
            init() {
                this.chart = this.$echarts.init(document.getElementById(this.id));
                this.chart.setOption(this.option);
                window.addEventListener("resize", this.chart.resize);
            }
        },
        watch: {
            //观察option的变化
            option: {
                handler(newVal, oldVal) {
                    if (this.chart) {
                        if (newVal) {
                            this.chart.setOption(newVal,true);
                        } else {
                            this.chart.setOption(oldVal,true);
                        }
                    } else {
                        this.init();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            }
        }
    };
</script>