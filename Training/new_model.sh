#!/bin/bash

echo
echo
echo '¡Hola, bienvenido!
Este programa se va a encargar de reunir todos los datos necesarios para crear un nuevo modelo de entrenamiento.
Lo primero que solicitará será el nombre del nuevo dataset. Ejemplo Temperatura.
El siguiente paso será solicitar los campos que servirán como modelo de entrenamiento. Introduzcalos en el mismo orden en el que se escribiran en el csv de entreanamiento.
Ejemplo Serie, Hora, Dia, Mes. (No use carácteres especiales).
Por último solicitará el campo a predecir. Ejemplo Temperatura.'
echo
echo


while [[ "$respuesta" != "si" ]]; do

	echo 'Introduzca el nombre del nuevo dataset (Ejemplo Temperatura):'
	read dataset
	echo

	campo=""
	ARRAY=()
	while [[ "$campo" != "fin" ]]; do

		echo 'Introduzca un nuevo campo de entrenamiento o escriba fin si no quiere añadir ninguno más:'
		read campo
		if [[ "$campo" != "fin" ]]; then
			ARRAY=("${ARRAY[@]}" $campo)
		fi


	done

	echo
	echo 'Introduzca el campo a predecir (Ejemplo Temperatura):'
	read to_predict


	echo
	echo "Estos son los datos introducidos:"
	echo "Nombre del dataset: $dataset"
	echo "Campos para el modelo de entrenamiento: ${ARRAY[@]}"
	echo "Campo a predecir: $to_predict"

	echo
	echo 'Si los datos son corretos, escriba si, de lo contrario escriba no:'
	read respuesta
	echo

done
ARRAY=("${ARRAY[@]}" "fin")

echo "Creando nuevo dataset..."
/usr/bin/php /Users/joseluis/PycharmProjects/SmartPolitech/training/new_model.php $dataset ${ARRAY[@]} $to_predict
echo "Nuevo dataset creado"
echo

echo "El siguente paso es añadir el csv de entrenamiento a la carpeta /SmartPolitech/training/ con el nombre training.csv"
while [[ "$respuesta" != "si" || ! -f training.csv ]]; do
  echo "Escriba si, si ya tiene el archivo añadido"
  read respuesta
  if [ ! -f training.csv ]; then
    echo "El fichero no existe, compruebe que se ha añadido a la carpeta /SmartPolitech/training/ y que el nombre es training.csv"
    echo
  fi
done

echo
echo "¿Desea iniciar ya el entrenamiento?"
read respuesta

cd ..
if [[ "$respuesta" == "si" ]]; then
  echo "Iniciando entrenamiento..."
  /usr/bin/python3 algorithms/earth/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/gaussiannaivebayes/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/isotonicregression/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/linearregression/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/linearregressionstatsmodel/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/logisticregression/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/randomforest/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/sgd/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/svr/model/model_trainer.py $PWD
  /usr/bin/python3 algorithms/xgboost/model/model_trainer.py $PWD
  echo "Entrenamiento finalizado"
fi

#Avisar al usuario que se ha terminado de ejecutar el script
echo ---------Fin del script.-------------
