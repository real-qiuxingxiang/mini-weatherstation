<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错

$servername = "Your IP";
$db_username = "Q";
$db_password = "~~~";
$dbname = "weather_station";
// 创建连接
$db = new mysqli($servername, $db_username, $db_password, $dbname);

//首页最新10条数据
$sql = "SELECT ". $_GET["column"] ." FROM node_1 ORDER BY time DESC";
//排序
if(isset($_GET["order"]) && $_GET["order"] != ""){
    //升序
    if($_GET["order"] == "increase"){
        $sql = "SELECT ". $_GET["column"] ." FROM node_1 ORDER BY time";
        if (isset($_GET["from_date"]) && isset($_GET["to_date"]) && $_GET["from_date"] != "" && $_GET["to_date"] != ""){
            $from_date = $_GET["from_date"] . " 00:00:00";
            $to_date = $_GET["to_date"] . " 23:59:59";

            $sql = "SELECT ". $_GET["column"] ." FROM node_1 WHERE time >= '" . $from_date . "' AND time <= '" . $to_date . "' ORDER BY time";
        }
    }
    //降序
    if($_GET["order"] == "decrease"){
        $sql = "SELECT ". $_GET["column"] ." FROM node_1 ORDER BY time DESC";
        if (isset($_GET["from_date"]) && isset($_GET["to_date"]) && $_GET["from_date"] != "" && $_GET["to_date"] != ""){
            $from_date = $_GET["from_date"] . " 00:00:00";
            $to_date = $_GET["to_date"] . " 23:59:59";

            $sql = "SELECT ". $_GET["column"] ." FROM node_1 WHERE time >= '" . $from_date . "' AND time <= '" . $to_date . "' ORDER BY time DESC";
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
