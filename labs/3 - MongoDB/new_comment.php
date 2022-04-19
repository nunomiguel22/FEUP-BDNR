<?php
require __DIR__ . '/vendor/autoload.php';
error_reporting(E_ALL);
ini_set('display_errors', 'On');
try {
        // Connect to the local Mongo server.
        $mongo = new MongoDB\Client();

        // Select a database (create if it doesn't exist).
        $topics = $mongo->selectDatabase('bdnr-php')->topics;

        $id = new MongoDB\BSON\ObjectID($_POST["topic"]);
        $text = $_POST["text"];
        $author = $_POST["author"];

        $new_comment = [
            'text' => $text,
            'author' => $author,
        ];

        // Insert documents to collection.
        $topics->updateMany(
            ["_id" => $id],
            ['$push' => ["comments" => $new_comment]]
        ); 

} catch (Exception $e) {
        print $e->getMessage();
};

?>