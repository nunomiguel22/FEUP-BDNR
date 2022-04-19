<html>
<h1>MiniForum</h1>

<a href="/index.php">Home</a>
<span> | </span>
<a href="/new_topic.html">Start a new topic!</a>
<hr>

<?php
if ($_GET["topic"]){
    include_once('topic.php');
}
else{
    include_once('home.php');
}

?>