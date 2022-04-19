<?php
require __DIR__ . '/vendor/autoload.php';

try {
        // Connect to the local Mongo server.
        $mongo = new MongoDB\Client();

        // Select a database (create if it doesn't exist).
        $db = $mongo->selectDatabase('bdnr-php');

        $title = $_POST["title"];
        $body = $_POST["body"];
        $author = $_POST["author"];

        // Select a collection.
        $topics = $db->topics;

        $new_topic = [
            'title' => $title,
            'body' => $body,
            'author' => $author,
            'comments' => []
        ];

        // Insert documents to collection.
        $insert = $topics->insertOne($new_topic);

        // Print insert information.
        print_r($insert);

} catch (Exception $e) {
        print $e->getMessage();
};

?>