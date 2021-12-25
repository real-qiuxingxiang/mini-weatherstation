<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错
include "JWT.php";

$username = $_GET["username"];
$password = $_GET["password"];

//连接数据库
$servername = "Your IP";
$db_username = "Q";
$db_password = "~~~";
$dbname = "weather_station";
// 创建连接
$db = new mysqli($servername, $db_username, $db_password,$dbname);
// 检测连接
if ($db->connect_error) {
    $json["status"] = "db_failed";
    die("连接失败: " . $db->connect_error);
}

$sql = "select Username,Password from users where Username = '$username' and Password = '$password'";
$result = $db->query($sql);
//统计执行结果影响的行数
//如果已经存在该用户
if ($result->num_rows){
    //将数据以索引的方式存储在数组中
    $row = mysqli_fetch_array($result);
    $_SESSION['username'] = $username;
    $json["status"] = "success";
    $db->close();
}else{
    $db->close();
    //弹出对话框后返回到先前页面
    $json["status"] = "failed";
}

$payload = array('iss'=>'Qiu','iat'=>time(),'exp'=>time()+7200,'nbf'=>time(),'sub'=>'Your IP/api','jti'=>md5(uniqid('JWT').time()));;
$json["token"] =JWT::getToken($payload);

echo json_encode($json);