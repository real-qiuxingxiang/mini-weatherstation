<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错

$servername = "Your IP";
$db_username = "Q";
$db_password = "~~~";
$dbname = "weather_station";
// 创建连接
$db = new mysqli($servername, $db_username, $db_password, $dbname);

//获取数据列表
$where = "";
if (isset($_GET["from_date"]) && isset($_GET["to_date"]) && $_GET["from_date"] != "" && $_GET["to_date"] != ""){
    $from_date = $_GET["from_date"] . " 00:00:00";
    $to_date = $_GET["to_date"] . " 23:59:59";

    $where .= " and time >= '" . $from_date . "' AND time <= '" . $to_date . "'";
}
if (isset($_GET["from_temperature"]) && isset($_GET["to_temperature"]) && $_GET["from_temperature"] != "" && $_GET["to_temperature"] != ""){
    $from_temperature = $_GET["from_temperature"];
    $to_temperature = $_GET["to_temperature"];

    $where .= " AND temperature >= " . $from_temperature . " AND temperature <= " . $to_temperature;
}
if (isset($_GET["from_humidity"]) && isset($_GET["to_humidity"]) && $_GET["from_humidity"] != "" && $_GET["to_humidity"] != ""){
    $from_humidity = $_GET["from_humidity"];
    $to_humidity = $_GET["to_humidity"];

    $where .= " AND humidity >= " . $from_humidity . " AND humidity <= " . $to_humidity;
}
if (isset($_GET["from_pressure"]) && isset($_GET["to_pressure"]) && $_GET["from_pressure"] != "" && $_GET["to_pressure"] != ""){
    $from_pressure = $_GET["from_pressure"];
    $to_pressure = $_GET["to_pressure"];

    $where .= " AND pressure >= " . $from_pressure . " AND pressure <= " . $to_pressure;
}
if (isset($_GET["from_wind_speed"]) && isset($_GET["to_wind_speed"]) && $_GET["from_wind_speed"] != "" && $_GET["to_wind_speed"] != ""){
    $from_wind_speed = $_GET["from_wind_speed"];
    $to_wind_speed = $_GET["to_wind_speed"];

    $where .= " AND wind_speed >= " . $from_wind_speed . " AND wind_speed <= " . $to_wind_speed;
}
if (isset($_GET["from_wind_direction"]) && isset($_GET["to_wind_direction"]) && $_GET["from_wind_direction"] != "" && $_GET["to_wind_direction"] != ""){
    $from_wind_direction = $_GET["from_wind_direction"];
    $to_wind_direction = $_GET["to_wind_direction"];

    $where .= " AND wind_direction >= " . $from_wind_direction . " AND wind_direction <= " . $to_wind_direction;
}

//分页数据
if (isset($_GET["offset"]) && $_GET["offset"] != "") {
    $sql = "SELECT * FROM node_1 ORDER BY time DESC LIMIT 10";
    //排序
    if(isset($_GET["order"]) && $_GET["order"] != ""){
        //升序
        if($_GET["order"] == "increase"){
            $sql = "SELECT * FROM node_1 ORDER BY time LIMIT 10 OFFSET ".$_GET["offset"];
            if($where != ""){
                $sql = "SELECT * FROM node_1 WHERE ". $where . " ORDER BY time LIMIT 10 OFFSET ". $_GET["offset"];
            }
        }
        //降序
        if($_GET["order"] == "decrease"){
            $sql = "SELECT * FROM node_1 ORDER BY time DESC LIMIT 10 OFFSET ".$_GET["offset"];
            if($where != ""){
                $sql = "SELECT * FROM node_1 WHERE time != '0' ". $where . " ORDER BY time DESC LIMIT 10 OFFSET ". $_GET["offset"];
            }
        }
    }
}

$data = $db->query($sql);

$arr = array();
while ($row = $data->fetch_assoc()) {
    $arr[] = $row;
}

//关闭连接
$db->close();
echo(json_encode($arr));
