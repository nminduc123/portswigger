<?php

session_start();
require "users.php";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $username = $_POST["username"];
    $password = $_POST["password"];

    if (
        isset($users[$username]) &&
        $users[$username]["password"] == $password
    ) {

        $_SESSION["username"] = $username;

        header("Location: upload.php");
        exit();
    }

    $error = "Login Failed";
}

?>

<!DOCTYPE html>
<html>

<head>
    <title>Login</title>
</head>

<body>

<h2>Login</h2>

<?php
if(isset($error)){
    echo "<p style='color:red;'>$error</p>";
}
?>

<form method="POST">

    Username <br>
    <input type="text" name="username">

    <br><br>

    Password <br>
    <input type="password" name="password">

    <br><br>

    <button type="submit">
        Login
    </button>

</form>

</body>
</html>