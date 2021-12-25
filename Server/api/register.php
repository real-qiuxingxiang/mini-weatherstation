<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错

$username = $_GET["username"];
$password = $_GET["password"];

//连接数据库
$servername = "Your IP";
$db_username = "Q";
$db_password = "~~~";
$dbname = "weather_station";

// 创建连接
$db = new mysqli($servername, $db_username, $db_password,$dbname);
if ($db->connect_error) {
    die("连接失败: " . $db->connect_error);
}

$result = $db->query("select Username from users where Username = '$username'");
//统计执行结果影响的行数
//$num = $result->num_rows;
//如果已经存在该用户
if($result->num_rows){
    echo "existed";
}else{
    //不存在当前注册用户名称
    $res_insert = $db->query("insert into users (Username,Password) values ('$username','$password')");
    if($res_insert){
        echo "success";
    }else{
        echo "failed";
        //history.go(-1);
    }
}
