<?php
include_once "../db/db_helper.php";

class cron_carga_inicial
{
    public function __construct()
    {

        $this->db = new _dbHelper();

    }

    private function load_csv()
    {
        $fila = 0;
        $conn = $this->db->connect_mysql();
        if (($gestor = fopen("file1.csv", "r")) !== FALSE) {
            while (($datos = fgetcsv($gestor, 1000, ",")) !== FALSE) {
                if ($fila > 0) {
                    //$datos[1] = $this->modify_date($datos[1]);
                    $this->insert_row($datos, $conn);
                }
                $fila++;
            }
            fclose($gestor);
        }
        $conn->close();

    }

//    private function fill_null_values()
//    {
//        $sql = "SELECT * FROM SmartPolitech.smart_data where value = 0";
//        $a_result = $this->db->select_data($sql);
//        foreach ($a_result as $result) {
//            $this->set_avg_value($result);
//        }
//    }

//    private function set_avg_value($row)
//    {
//        $prefix_date = "%" . substr($row[2], 5, 8) . "%";
//        $sql = "SELECT avg(value)
//                FROM SmartPolitech.smart_data
//                WHERE date_event like '$prefix_date'
//                    AND series_name = '{$row['1']}'
//                    AND value <> 0";
//        $value = $this->db->select_data($sql)[0][0];
//
//        if ($value) {
//            $sql = "UPDATE SmartPolitech.smart_data
//                SET value = '$value'
//                WHERE id={$row[0]}";
//            $this->db->insert_update_data($sql);
//        }
//
//    }
//
//
//    private function modify_date($date)
//    {
//
//
//        $a_date = substr($date, 0, 10);
//        $date = date("Y-m-d", strtotime($a_date));
//        return $date;
//
//    }

    private function insert_row($row, $conn)
    {

//        $name = $row[0];
//        $date = $row[1];
//         $value = floatval($row[2]);
//        $season = $this->get_season($date);
        $date = $row[0] . "-" . $row[1] . "-" . $row[2];

        $sql = "INSERT INTO smart_data (date,year,month,day,temperature,humidity,wind_speed,pressure,precipitation)
                 VALUES ('$date', $row[0], $row[1], $row[2], $row[3], $row[4], $row[5], $row[6], $row[7])";

        $this->db->insert_update_data_multiple($sql, $conn);

    }

//    private function get_season($date)
//    {
//        $month = substr($date, 5, 2);
//        if ($month == "03" || $month == "04" || $month == "05")
//            return 1;
//        if ($month == "06" || $month == "07" || $month == "08")
//            return 2;
//        if ($month == "09" || $month == "10" || $month == "11")
//            return 3;
//        if ($month == "12" || $month == "01" || $month == "02")
//            return 4;
//    }

    public function run()
    {
        $this->load_csv();
        //$this->fill_null_values();
    }
}

$a = new cron_carga_inicial();
$a->run();