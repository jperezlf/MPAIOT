<?php

include_once "../db/db_helper.php";

$name_dataset = $argv[1];

$model_trainer_field = array();

for ($i = 2; $argv[$i] != "fin"; $i++) {
    $model_trainer_field[] = $argv[$i];
}
$model_trainer_field = json_encode($model_trainer_field, true);

$predict_field = $argv[$i + 1];

$db = new _dbHelper();
$sql = "INSERT INTO smart_dataset (name_dataset, model_trainer_field, predict_field)
        VALUES ('$name_dataset', '$model_trainer_field', '$predict_field')";
$conn = $db->connect_mysql();
$db->insert_update_data($sql, $conn);

