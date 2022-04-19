
<?php
session_start();
require __DIR__ . '/vendor/autoload.php';

Predis\Autoloader::register();

try {
	// Connect to the localhost Redis server.
	$redis = new Predis\Client();

    $user_password = $redis->hget("users:" . $_POST["username"], "password");


    if (password_verify($_POST["password"], $user_password)){
        $_SESSION["LOGIN"] = true;
        $_SESSION["USERNAME"] = $_POST["username"];
        echo "SUCCESS";
    }
    else {
        echo "FAILED";
    }

} catch (Exception $e) {
	print $e->getMessage();
};

?>
