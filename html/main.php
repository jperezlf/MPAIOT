<?php

include_once "../db/db_helper.php";
include_once "../algorithms/execute_algorithm.php";

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

    public function get_data_xgboost()
    {
        $xgboost = new execute_algorithm("xgboost");
        echo json_encode($xgboost->run());
    }

    public function get_data_linregmult()
    {
        $linearregresion = new execute_algorithm("linearregression");
        echo json_encode($linearregresion->run());
    }

    public function get_data_linregmultstastmodel()
    {
        $linearregresionstatsmodel = new execute_algorithm("linearregressionstatsmodel");
        echo json_encode($linearregresionstatsmodel->run());
    }

    public function get_data_randomforest()
    {
        $randomforest = new execute_algorithm("randomforest");
        echo json_encode($randomforest->run());
    }

    public function get_data_svr()
    {
        $svr = new execute_algorithm("svr");
        echo json_encode($svr->run());
    }

    public function get_data_logisticregression()
    {
        $logisticregression = new execute_algorithm("logisticregression");
        echo json_encode($logisticregression->run());
    }

    public function get_data_stochasticgradientdescent()
    {
        $stochasticgradientdescent = new execute_algorithm("sgd");
        echo json_encode($stochasticgradientdescent->run());
    }

    public function get_data_bart()
    {
        $bart = new execute_algorithm("bart");
        echo json_encode($bart->run());
    }

    public function get_data_gaussiannaivebayes()
    {
        $gaussiannaivebayes = new execute_algorithm("gaussiannaivebayes");
        echo json_encode($gaussiannaivebayes->run());
    }

    public function get_data_isotonicregression()
    {
        $isotonicregression = new execute_algorithm("isotonicregression");
        echo json_encode($isotonicregression->run());
    }


}


$main = new main();

if (isset($_GET['function'])) {
    $action = $_GET['function'];

    switch ($action) {
        case "show_fields":
            $main->show_fields();
            break;
        case "get_data_xgboost":
            $main->get_data_xgboost();
            break;
        case "get_data_linregmult":
            $main->get_data_linregmult();
            break;
        case "get_data_linregmultstastmodel":
            $main->get_data_linregmultstastmodel();
            break;
        case "get_data_randomforest":
            $main->get_data_randomforest();
            break;
        case "get_data_svr":
            $main->get_data_svr();
            break;
        case "get_data_logisticregression":
            $main->get_data_logisticregression();
            break;
        case "get_data_stochasticgradientdescent":
            $main->get_data_stochasticgradientdescent();
            break;
        case "get_data_bart":
            $main->get_data_bart();
            break;
        case "get_data_gaussiannaivebayes":
            $main->get_data_gaussiannaivebayes();
            break;
        case "get_data_isotonicregression":
            $main->get_data_isotonicregression();
            break;

        default:
        {
            // do not forget to return default data, if you need it...
        }
    }
}

?>