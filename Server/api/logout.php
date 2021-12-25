<html>
<head>
    <!-- 解决弹窗对话框乱码问题 -->
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<?php
session_start();
$_SESSION['username'] = null;
header('Location:../login.html');
