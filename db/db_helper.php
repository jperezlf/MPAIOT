<?php


class _dbHelper
{

    public function __construct()
    {

    }

    public function connect_mysql()
    {

        $servername = "127.0.0.1";
        $username = "root";
        $password = "61016101";


        // Create connection
        $conn = new mysqli($servername, $username,$password, "SmartPolitech");

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        //echo "Connected successfully";

        return $conn;

    }

    public function select_data($sql)
    {
        $conn = $this->connect_mysql();

        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            $result = $result->fetch_all();
            $conn->close();
            return $result;
        }
    }

    public function insert_update_data($sql)
    {
        $conn = $this->connect_mysql();
        if ($conn->query($sql) != TRUE) {
            print_r("Error: " . $sql . "<br>" . $conn->error);
        }

        $conn->close();
    }

    public function insert_update_data_multiple($sql, $conn)
    {
        if ($conn->query($sql) != TRUE) {
            print_r("Error: " . $sql . "<br>" . $conn->error);
        }
    }


}

$a = new _dbHelper();
$a->connect_mysql();
