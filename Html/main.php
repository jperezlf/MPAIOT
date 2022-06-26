<?php

include_once "../Db/db_helper.php";
include_once "../Algorithms/execute_algorithm.php";
include_once "../Algorithms/execute_algorithm_dos.php";
include_once "paint_file.php";

class main
{
    public function __construct()
    {
        $this->db = new _dbHelper();
    }

    public function show_fields()
    {
        $a_data_tag = array();
        $a_data_tag = $this->create_fields($a_data_tag);
        echo json_encode($a_data_tag);
    }

    private function create_fields($a_data_tag)
    {
        $sql = "SELECT name_series from smart_series";
        $result = $this->db->select_data($sql);
        $a_data_tag['name_series']['data'][0]['value'] = 'Series';
        $a_data_tag['name_series']['data'][0]['key'] = 'name_series';
        foreach ($result as $key => $r) {
            $key++;
            $a_data_tag['name_series']['data'][$key]['value'] = $r[0];
            $a_data_tag['name_series']['data'][$key]['key'] = 'name_series';
        }

        $sql = "SELECT name_algorithm from smart_algorithms";
        $result = $this->db->select_data($sql);
        $a_data_tag['name_algorithms']['data'][0]['value'] = 'All Algorithms';
        $a_data_tag['name_algorithms']['data'][0]['key'] = 'name_algorithms';
        foreach ($result as $key => $r) {
            $key++;
            $a_data_tag['name_algorithms']['data'][$key]['value'] = $r[0];
            $a_data_tag['name_algorithms']['data'][$key]['key'] = 'name_algorithm';
        }

        $sql = "SELECT name_dataset from smart_dataset";
        $result = $this->db->select_data($sql);
        foreach ($result as $key => $r) {
            $a_data_tag['dataset']['data'][$key]['value'] = $r[0];
            $a_data_tag['dataset']['data'][$key]['key'] = 'dataset';
        }

        return $a_data_tag;
    }

    public function getDataXgboost()
    {
        $xgboost = new execute_algorithm_dos("xgboost");
        echo json_encode($xgboost->run());
    }

    public function getDataLinearRegression()
    {
        $linearRegresion = new execute_algorithm_dos("linearRegression");
        echo json_encode($linearRegresion->run());
    }

    public function getDataRandomForest()
    {
        $randomForest = new execute_algorithm_dos("randomForest");
        echo json_encode($randomForest->run());
    }

    public function getDataSVR()
    {
        $svr = new execute_algorithm_dos("svr");
        echo json_encode($svr->run());
    }

    public function getDataElasticNet()
    {
        $elasticNet = new execute_algorithm_dos("elasticNet");
        echo json_encode($elasticNet->run());
    }

    public function getDataStochasticGradientDescent()
    {
        $stochasticGradientDescent = new execute_algorithm_dos("sgd");
        echo json_encode($stochasticGradientDescent->run());
    }

    public function getDataRidge()
    {
        $ridge = new execute_algorithm_dos("ridge");
        echo json_encode($ridge->run());
    }

    public function getDataDecisionTreeRegressor()
    {
        $decisionTreeRegressor = new execute_algorithm_dos("decisionTreeRegressor");
        echo json_encode($decisionTreeRegressor->run());
    }

    public function getDataLasso()
    {
        $lasso = new execute_algorithm_dos("lasso");
        echo json_encode($lasso->run());
    }

    public function getDataRobustRegression()
    {
        $robustRegression = new execute_algorithm_dos("robustRegression");
        echo json_encode($robustRegression->run());
    }
}

$main = new main();

if (isset($_FILES['file'])) {
    $file = $_FILES['file']['tmp_name'];

    $paint_file = new Paint_file();
    echo json_encode($paint_file->run($file));
}

if (isset($_GET['function'])) {
    $action = $_GET['function'];

    switch ($action) {
        case "show_fields":
            $main->show_fields();
            break;
        case "getDataXgboost":
            $main->getDataXgboost();
            break;
        case "getDataLinearRegression":
            $main->getDataLinearRegression();
            break;
        case "getDataRandomForest":
            $main->getDataRandomForest();
            break;
        case "getDataSVR":
            $main->getDataSVR();
            break;
        case "getDataElasticNet":
            $main->getDataElasticNet();
            break;
        case "getDataStochasticGradientDescent":
            $main->getDataStochasticGradientDescent();
            break;
        case "getDataRidge":
            $main->getDataRidge();
            break;
        case "getDataDecisionTreeRegressor":
            $main->getDataDecisionTreeRegressor();
            break;
        case "getDataLasso":
            $main->getDataLasso();
            break;
        case "getDataRobustRegression":
            $main->getDataRobustRegression();
            break;
    }
}

?>