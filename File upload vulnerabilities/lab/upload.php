<?php

session_start();

if (!isset($_SESSION["username"])) {
    header("Location: login.php");
    exit();
}

$message = "";

// Upload
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $file = $_FILES["avatar"];

    $filename = basename($file["name"]);
    $tmp = $file["tmp_name"];
    $contentType = $file["type"];

    // Lấy đuôi file
    $extension = strtolower(pathinfo($filename, PATHINFO_EXTENSION));

    /*
        VULNERABLE
        Chỉ kiểm tra Content-Type
    */
    if (
        $contentType == "image/jpeg" ||
        $contentType == "image/png"
    ) {

        // Lưu theo tên user
        $newName = $_SESSION["username"] . "." . $extension;

        move_uploaded_file(
            $tmp,
            "uploads/" . $newName
        );

        $message = "Upload Success";

    } else {

        $message = "Only JPG / PNG";

    }
}

?>

<!DOCTYPE html>
<html>

<head>
    <title>Upload Avatar</title>
</head>

<body>

<h1>
Welcome <?php echo $_SESSION["username"]; ?>
</h1>

<a href="logout.php">Logout</a>

<hr>

<?php

$avatarJpg = "uploads/" . $_SESSION["username"] . ".jpg";
$avatarPng = "uploads/" . $_SESSION["username"] . ".png";

if (file_exists($avatarJpg)) {

    echo "<img src='$avatarJpg' width='180'><br><br>";

}
elseif (file_exists($avatarPng)) {

    echo "<img src='$avatarPng' width='180'><br><br>";

}

?>

<?php
echo $message;
?>

<form
method="POST"
enctype="multipart/form-data">

<input
type="file"
name="avatar">

<br><br>

<button type="submit">
Upload
</button>

</form>

</body>
</html>