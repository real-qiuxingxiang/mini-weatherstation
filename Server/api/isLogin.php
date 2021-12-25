<?php
header("Access-Control-Allow-Origin: *");//这个必写，否则报错
include "JWT.php";

$token = $_GET["token"];
echo JWT::verifyToken($token);