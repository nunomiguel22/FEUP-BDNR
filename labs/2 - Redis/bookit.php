<?php
session_start();
require __DIR__ . '/vendor/autoload.php';

Predis\Autoloader::register();

try {
	// Connect to the localhost Redis server.
	$redis = new Predis\Client();

    $timestamp = time();
    $url = $_POST["url"];
    $bookmark_hash = hash("md5", $url);
    $tags = explode(",", $_POST["tags"]);

    /**
     * bookmark:id url -> hash with url
     * bookmark:id:tags -> set with tags
     * bookmarks -> sorted set with bookmark id ordered by timestamp
     * tag:tagname -> set of bookmarks associated to the tag
     */

    $bookmark_prefix ="bookmark:" . $bookmark_hash;
    $redis->hset($bookmark_prefix, "url", $url);
    print_r($_SESSION["USERNAME"]);
    $redis->sadd($bookmark_prefix . ":users", $_SESSION["USERNAME"]);

    $redis->zadd("users:" . $_SESSION["USERNAME"] . ":bookmarks", $timestamp, $bookmark_hash);

    foreach ($tags as $tag){
        $redis->sadd($bookmark_prefix . ":tags:" . $_SESSION["USERNAME"], $tag);
        $redis->sadd("users:" . $_SESSION["USERNAME"] . ":tag:" . $tag, $bookmark_hash);
    }

} catch (Exception $e) {
	print $e->getMessage();
};

?>
