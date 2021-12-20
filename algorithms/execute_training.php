<?php

include_once "../../db/db_helper.php";

class execute_training
{

    public function run()
    {
        $algorithms = array("earth",
            "gaussiannaivebayes",
            "isotonicregression",
            "linearregression",
            "linearregressionstatsmodel",
            "logisticregression",
            "randomforest",
            "sgd",
            "svr",
            "xgboost");
        foreach ($algorithms as $algorithm) {
            $command = "cd .. && cd algorithms/$algorithm/model/ && python3 model_trainer.py /Users/joseluis/PycharmProjects/SmartPolitech";
            $result = shell_exec($command);
        }
    }


}

$a = new execute_training();
$a->run();