<template>
    <div id="app">
        <NavigationBar :isChartActive="true"/>
        <ChartFilter :filter_option="filter_option" @filter_option_changed="filter_option_changed"/>
        <RenderChart id="LineChart" :option="option"/>
    </div>
</template>

<script>
    import RenderChart from "../components/RenderChart";
    import NavigationBar from "../components/NavigationBar";
    import ChartFilter from "../components/ChartFilter";
    import axios from "axios";

    export default {
        name: "ChartApp",
        components: {
            RenderChart,
            NavigationBar,
            ChartFilter
        },
        data() {
            return {
                filter_option: {
                    checkedData: ["temperature"],
                    page: 1,
                    offset: 0,
                    from_date: '',
                    to_date: '',
                    order: 'decrease',
                },
                option: {
                    dataZoom: [
                        {
                            id: 'dataZoomX',
                            type: 'slider',
                            xAxisIndex: [0],
                            filterMode: 'filter',
                            start: 30,
                            end: 70
                        },
                        {
                            id: 'dataZoomY',
                            type: 'slider',
                            yAxisIndex: [0],
                            filterMode: 'empty'
                        }
                    ],
                    tooltip: {
                        show: true,
                        trigger: 'axis'
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
                }
            }
        },
        created () {

        },
        mounted() {
            this.refresh_chart()
        },
        methods: {
            refresh_chart () {
                this.option.xAxis.data.length = 0
                this.option.series = []
                this.option.legend.data = []
                let checked = ""
                for(let i = 0; i < this.filter_option.checkedData.length; i++){
                    this.option.series.push({
                        name: this.filter_option.checkedData[i],
                        type: "line",
                        data: [],
                        itemStyle : { normal: {label : {show: true}}}
                    })
                    this.option.legend.data.push(this.filter_option.checkedData[i])
                    checked = checked + ',' + this.filter_option.checkedData[i]
                }
                axios
                    .get("https://Your IP/api/chartData.php?column=time" + checked + "&offset=" + this.filter_option.offset + "&from_date=" + this.filter_option.from_date + "&to_date=" + this.filter_option.to_date + "&order=" + this.filter_option.order)
                    .then((response) => {
                        for (let i = 0; i < response["data"].length; i++) {
                            this.option.xAxis.data.push(response["data"][i]["time"])
                        }
                        for(let j = 0; j < this.filter_option.checkedData.length; j++) {
                            for (let i = 0; i < response["data"].length; i++) {
                                this.option.series[j].data.push(response["data"][i][this.filter_option.checkedData[j]])
                            }
                        }
                    })
                    .catch(function (error) { // 请求失败处理
                        console.log(error);
                    });
            },
            filter_option_changed (msg){
                this.filter_option = msg
                this.refresh_chart()
            }
        }
    };
</script>