<?php

require __DIR__ . '/vendor/autoload.php';

try {
        // Connect to the local Mongo server.
        $mongo = new MongoDB\Client();

        // Select the collection.
        $collection = $mongo->selectDatabase('bdnr-php')->topics;
        $id = new MongoDB\BSON\ObjectID($_GET["topic"]);

        $query = ['_id' => $id];

        $topic = $collection->findOne($query);

        echo '<h1>' . $topic->title . '</h1>';
        echo '<br>';
        echo '<span>' . $topic->body . '</span>';
        echo '<br>';
        echo '<hr>';
        echo '<h2>Comments</h2>';
        
        foreach ($topic->comments as $comment){
            echo '<p>';
            echo $comment->text;
            echo ' | ';
            echo $comment->author;
            echo '</p>';
        }


} catch (Exception $e) {
        print $e->getMessage();
};
?>

<form action="/new_comment.php" method="post">
    <input type="hidden" name="topic" value="<?php echo $_GET["topic"]; ?>">
    <textarea name="text" id="" cols="30" rows="10"></textarea>
    <br>
    <label for="author">Author</label>
    <br>
    <input type="text" name="author">
    <br><br>
    <button type="submit">Submit</button>
</form>