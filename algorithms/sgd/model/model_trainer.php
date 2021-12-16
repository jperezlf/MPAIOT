<?php

include_once "../../../db/db_helper.php";

class model_trainer
{

    public function __construct()
    {
        $this->db = new _dbHelper();

    }

    private function get_data()
    {

        $sql = "SELECT id_series, SUBSTRING(date_event, 12, 2) as hour ,SUBSTRING(date_event, 9, 2) as day, SUBSTRING(date_event, 6, 2) as month, value
                FROM SmartPolitech.smart_data
                INNER JOIN SmartPolitech.smart_series on series_name = name_series";
        $data = $this->db->select_data($sql);
        return $data;

    }

    private function create_csv($data)
    {
        array_unshift($data, array("serie", "hour", "day", "month", "value"));

        $fp = fopen('training.csv', 'wb');
        foreach ($data as $line) {
            fputcsv($fp, $line);
        }
        fclose($fp);


    }


    public function run()
    {
        $data = $this->get_data();
        $this->create_csv($data);
        print_r(exec("python3 model_trainer.py"));


    }

}


$a = new model_trainer();
$a->run();