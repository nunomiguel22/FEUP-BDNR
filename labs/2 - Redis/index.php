<html>
    <h1>BOOKIT</h1>
    <h2>Latest Bookmarks</h2>
    <hr>
</html>

<?php
require __DIR__ . '/vendor/autoload.php';

Predis\Autoloader::register();

try {
	// Connect to the localhost Redis server.
	$redis = new Predis\Client();
    $bookmarks = null;
    if (is_null($_GET["tag"])){
        $bookmarks = $redis->zrevrange("bookmarks", 0, 14);
    }
    else {
        $inter_tags = explode(",", $_GET["tag"]);
        foreach($inter_tags as &$tag){
            $tag = 'tag:' . $tag;
        }
        $bookmarks = $redis->sinter($inter_tags);
    }

    foreach($bookmarks as $bookmark_id){
        $url = $redis->hget("bookmark:" . $bookmark_id, "url");
        $tags = $redis->smembers("bookmark:" . $bookmark_id . ":tags");
        echo '<div>';
        echo '<a href="' .  $url . '">' . $url .'</a>';

        echo '<div>[';
        foreach ($tags as $tag){
            echo '<a href="/?tag=' .  $tag . '">' . $tag .' </a>';
        }
        echo ']</div>';

        echo '</div>';
        echo '<br>';
    }

    echo '<hr>';
    echo '<a href="/">Home </a>';
    echo '|';
    echo '<a href="/add.html"> Add another bookmark! </a>';
} catch (Exception $e) {
	print $e->getMessage();
};
?>
