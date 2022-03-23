<?php

require __DIR__ . '/vendor/autoload.php';

Predis\Autoloader::register();

try {
	// Connect to the localhost Redis server.
	$redis = new Predis\Client();

    $bookmark_id = $redis->incr("next_bookmark_id");
    $timestamp = time();
    $url = $_POST["url"];
    $tags = explode(",", $_POST["tags"]);

    /**
     * bookmark:id url -> hash with url
     * bookmark:id:tags -> set with tags
     * bookmarks -> sorted set with bookmark id ordered by timestamp
     * tag:tagname -> set of bookmarks associated to the tag
     */

    $bookmark_prefix ="bookmark:" . $bookmark_id;

    $redis->hset($bookmark_prefix, "url", $url);
    $redis->zadd("bookmarks", $timestamp, $bookmark_id);

    foreach ($tags as $tag){
        $redis->sadd($bookmark_prefix . ":tags", $tag);
        $redis->sadd("tag:" . $tag, $bookmark_id);
    }

} catch (Exception $e) {
	print $e->getMessage();
};

?>
