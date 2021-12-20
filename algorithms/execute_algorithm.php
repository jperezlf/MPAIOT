<?php

include_once "../../db/db_helper.php";

class execute_algorithm
{

    public function __construct($type)
    {
        $this->db = new _dbHelper();
        $this->type = $type;
    }


    private function get_data()
    {
        $series_name = $_GET['series_name'];
        $dateStart = $_GET['date'];

        $dateEnd = date('Y-m-d', strtotime("+ 1 day"));
        $array = array();

        while ($dateStart < $dateEnd) {

            $tomorrow = date('Y-m-d', strtotime($dateStart . "+1 day"));
            $sql = "SELECT * from SmartPolitech.smart_data where date_event >= '$dateStart' and date_event < '$tomorrow' and series_name = '$series_name'";

            $a_result = $this->db->select_data($sql);

            $array_data[0]['name'] = 'Temperatura';
            foreach ($a_result as $result) {
                $array = array();
                $array[] = $result[2];
                $array[] = floatval($result[3]);
                $array_data[0]['data'][] = $array;
                $array_data[0]['marker']['enabled'] = false;
            }
            $dateStart = date('Y-m-d', strtotime($dateStart . "+1 day"));
        }

        $i = 0;
        $dateStart = $_GET['date'];
        $prediction = $this->get_prediction();
        while ($i < count($prediction)) {
            $array = array();
            $array[] = $dateStart . ' 02:00:00';
            if (isset($prediction[$i][0]))
                $array[] = $prediction[$i][0];
            else
                $array[] = $prediction[$i];
            $array_prediction[] = $array;
            $i++;
//             $array = array();
//             $array[] = $dateStart . ' 14:00:00';
//             $array[] = $prediction[$i];
//             $array_prediction[] = $array;
//             $i++;
            $dateStart = date('Y-m-d', strtotime($dateStart . '+1 day'));
        }

        $array_data[1]['name'] = 'Temperatura Prediction';
        $array_data[1]['color'] = '#7CB5EC';
        $array_data[1]['lineWidth'] = 1;
        $array_data[1]['dashStyle'] = "longdash";
        $array_data[1]['marker']['enabled'] = false;
        $array_data[1]['name'];
        $array_data[1]['data'] = $array_prediction;

        return $array_data;
    }


    private function get_prediction()
    {
        $dateStart = $_GET['date'];
        $interval = $_GET['days_prediction'];
        //$interval = $interval * 2;
        $series_id = $this->get_id_serie_by_name($_GET['series_name']);
        $array_data = array();


        for ($i = 0; $i < $interval; $i++) {
            $hour = "02";
            $day = substr($dateStart, 8, 2);
            $month = substr($dateStart, 5, 2);
            $array = json_encode(array($day, $hour, $month, $series_id));
            $array_data[] = $array;
//            $hour = "14";
//            $array = json_encode(array($day, $hour, $month, $series_id));
//            $array_data[] = $array;

            $dateStart = date('Y-m-d', strtotime($dateStart . "+1 day"));
        }

        $array_data = json_encode($array_data);

        $command = "cd .. && cd algorithms/$this->type/model/ && /usr/local/bin/python3 charge_model.py " . $array_data;
        $result = shell_exec($command);

        $result = json_decode($result);

        return $result;


    }

    private function get_id_serie_by_name($serie_name)
    {
        $sql = "SELECT id_series 
                FROM SmartPolitech.smart_series 
                WHERE name_series = '$serie_name'";
        $result = $this->db->select_data($sql);
        return $result[0][0];
    }

    public function run()
    {
        return $this->get_data();
    }


}