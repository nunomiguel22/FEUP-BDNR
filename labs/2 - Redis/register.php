
<?php

require __DIR__ . '/vendor/autoload.php';

Predis\Autoloader::register();

try {
	// Connect to the localhost Redis server.
	$redis = new Predis\Client();

    $pass_hash = password_hash($_POST["password"], PASSWORD_BCRYPT);

    $redis->hset('users:' . $_POST["username"], "password", $pass_hash);

} catch (Exception $e) {
	print $e->getMessage();
};

?>
