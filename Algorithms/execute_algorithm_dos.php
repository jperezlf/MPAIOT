<?php

include_once "../../db/db_helper.php";

class execute_algorithm_dos
{

    public function __construct($type)
    {
        $this->db = new _dbHelper();
        $this->type = $type;
    }


    private function get_data()
    {

        $dateStart = $_GET['date'];
        $dateEnd = date('Y-m-d', strtotime("+ 1 day"));

        while ($dateStart < $dateEnd) {

            $tomorrow = date('Y-m-d', strtotime($dateStart . "+1 day"));

            $sql = "SELECT *
                    FROM SmartPolitech.smart_data 
                    WHERE date >= '$dateStart' and date < '$tomorrow'";

            $a_result = $this->db->select_data($sql);

            $array_data[0]['name'] = 'Temperature';
            foreach ($a_result as $result) {
                $array = array();
                $array[] = $result[1];
                $array[] = floatval($result[5]);
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
            $array[] = $dateStart;
            if (isset($prediction[$i][0]))
                $array[] = $prediction[$i][0];
            else
                $array[] = $prediction[$i];
            $array_prediction[] = $array;
            $i++;

            $dateStart = date('Y-m-d', strtotime($dateStart . '+1 day'));
        }

        $array_data[1]['name'] = 'Temperature Prediction';
        $array_data[1]['color'] = '#7CB5EC';
        $array_data[1]['lineWidth'] = 1;
        $array_data[1]['dashStyle'] = "longdash";
        $array_data[1]['marker']['enabled'] = false;
        $array_data[1]['data'] = $array_prediction;


        return $array_data;
    }


    private function get_prediction()
    {
        $dateStart = $_GET['date'];
        $interval = $_GET['days_prediction'];
        $array_data = array();

        for ($i = 0; $i < $interval; $i++) {
            $day = substr($dateStart, 8, 2);
            $month = substr($dateStart, 5, 2);
            $year = substr($dateStart, 0, 4);

            $sql = "SELECT  dew_point, 
                                humidity, 
                                wind_speed, 
                                pressure
                    FROM SmartPolitech.smart_data
                    WHERE month=$month
                        AND day=$day
                        AND year =$year";
            $result = $this->db->select_data($sql);
            if (!isset($result[0][0])) {
                $sql = "SELECT avg(dew_point), 
                                avg(humidity), 
                                avg(wind_speed), 
                                avg(pressure)
                    FROM SmartPolitech.smart_data
                    WHERE month=$month
                        AND day=$day
                        AND year > '2020'";
                $result = $this->db->select_data($sql);
            }

            $dew_point = $result[0][0];
            $humidity = $result[0][1];
            $wind_speed = $result[0][2];
            $pressure = $result[0][3];
            $array = json_encode(array($day, $dew_point, $humidity, $month, $pressure, $wind_speed, $year));

            $array_data[] = $array;

            $dateStart = date('Y-m-d', strtotime($dateStart . "+1 day"));
        }

        $array_data = json_encode($array_data);

        $command = "cd .. && cd algorithms/$this->type/model/ && /usr/local/bin/python3 charge_model.py " . $array_data;

        $result = shell_exec($command);

        $result = json_decode($result);

        return $result;
    }

    public function run()
    {
        return $this->get_data();
    }


}