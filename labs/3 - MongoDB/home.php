<h2>Topics</h2>
</html>

<?php

require __DIR__ . '/vendor/autoload.php';

try {
        // Connect to the local Mongo server.
        $mongo = new MongoDB\Client();

        // Select the collection.
        $collection = $mongo->selectDatabase('bdnr-php')->topics;

        // Create a cursor to iterate over the complete collection.
        $cursor = $collection->find();

        // Go through each record.
        foreach ($cursor as $result) {
                $link = '<a href=index.php?topic=' . $result->_id . '>' . $result->title . "</a>";
                echo $link;

                if ($result->comments->Count()){
                    echo '(' . $result->comments->Count() . " comments)";
                }

                echo '<br>';
        }


} catch (Exception $e) {
        print $e->getMessage();
};

?>