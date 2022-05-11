<?php

class Paint_file
{
    public function __construct()
    {

    }

    private function file_to_array($file)
    {
        $array = [];
        if (($gestor = fopen($file, "r")) !== FALSE) {
            while (($datos = fgetcsv($gestor, 1000, ";")) !== FALSE) {
                $array[] = $datos;
            }
        }
        return $array;
    }

    private function format_array($array)
    {
        $num_algorithm = sizeof($array[0]) / 4;
        $index = 2;
        for ($i = 0; $i < $num_algorithm; $i++) {
            $array_to_paint = [];
            $array_to_paint[0]["name"] = $array[0][$index];
            $array_to_paint[0]['marker']['enabled'] = false;

            $data = [];
            foreach ($array as $key => $a) {
                if ($key > 0 && !empty($a[$index])) {
                    $data[$key - 1][0] = $a[$index - 1];
                    $data[$key - 1][1] = floatval(str_replace(",", ".", $a[$index]));
                }
            }
            $array_to_paint[0]['data'] = $data;


            $array_to_paint[1]["name"] = $array[0][$index + 1];
            $array_to_paint[1]['color'] = '#7CB5EC';
            $array_to_paint[1]['lineWidth'] = 1;
            $array_to_paint[1]['dashStyle'] = "longdash";
            $array_to_paint[1]['marker']['enabled'] = false;

            $data = [];
            foreach ($array as $key => $a) {
                if ($key > 0 && !empty($a[$index + 1])) {
                    $data[$key - 1][0] = $a[$index - 1];
                    $data[$key - 1][1] = floatval(str_replace(",", ".", $a[$index + 1]));
                }
            }
            $array_to_paint[1]['data'] = $data;
            $array_to_paint[2]['name_algorithm'] = $array[1][$index - 2];

            $a_array_to_paint[] = $array_to_paint;

            $index = $index + 4;
        }

        return $a_array_to_paint;

    }


    public function run($file)
    {
        $array = $this->file_to_array($file);
        $array = $this->format_array($array);


        return $array;


    }

}