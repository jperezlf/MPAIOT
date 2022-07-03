<?php
include_once "../Db/db_helper.php";

class loaddatadb
{
    public function __construct()
    {

        $this->db = new _dbHelper();

    }

    private function load_csv()
    {
        $fila = 0;
        $conn = $this->db->connect_mysql();
        if (($gestor = fopen("../Files/Dataset.csv", "r")) !== FALSE) {
            while (($datos = fgetcsv($gestor, 1000, ",")) !== FALSE) {
                if ($fila > 0) {
                    $this->insert_row($datos, $conn);
                }
                $fila++;
            }
            fclose($gestor);
        }
        $conn->close();

    }

    private function insert_row($row, $conn)
    {

        $date = date("Y-m-d", strtotime($row[0] . "-" . $row[1] . "-" . $row[2]));

        $sql = "INSERT INTO smart_data (date, year, month, day, temperature, dew_point, humidity, wind_speed, pressure)
                 VALUES ('$date', $row[0], $row[1], $row[2], $row[3], $row[4], $row[5], $row[6], $row[7])";

        $this->db->insert_update_data_multiple($sql, $conn);

    }

    public function run()
    {
        $this->load_csv();
    }
}

$a = new loaddatadb();
$a->run();