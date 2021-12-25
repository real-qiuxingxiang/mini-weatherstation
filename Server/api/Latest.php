<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错

$servername = "Your IP";
$db_username = "Q";
$db_password = "~~~";
$dbname = "weather_station";
// 创建连接
$db = new mysqli($servername, $db_username, $db_password, $dbname);

//获取开关设置
$sql = "SELECT * FROM node_1 ORDER BY time DESC LIMIT 1";
$data = $db->query($sql);
$arr = array();

while ($row = $data->fetch_assoc()) {
    $arr[] = $row;
}

//关闭连接
$db->close();
echo(json_encode($arr));
