function main() {
    _init_date_picker();
    _init_fields();
    _init_events();
    fillConfig(1)


    console.log("Iniciando renderizado")
}


function _init_functions() {

    return [
        {"function_data": "getDataXgboost", "name_algorithm": "XGBoost"},
        {"function_data": "getDataLinearRegression", "name_algorithm": "Linear Regression"},
        {"function_data": "getDataRandomForest", "name_algorithm": "Ramdom Forest"},
        {"function_data": "getDataSVR", "name_algorithm": "Support Vector Regression"},
        {"function_data": "getDataElasticNet", "name_algorithm": "Elastic Net Regression"},
        {"function_data": "getDataStochasticGradientDescent", "name_algorithm": "Stochastic Gradient Descent"},
        {"function_data": "getDataLasso", "name_algorithm": "LASSO Regression"},
        {"function_data": "getDataRidge", "name_algorithm": "Ridge Regression"},
        {"function_data": "getDataDecisionTreeRegressor", "name_algorithm": "Decision Tree Regressor"},
        {"function_data": "getDataRobustRegression", "name_algorithm": "Robust Regression RANSAC"},
    ]
}

function charge_algorithm(selected) {
    var functions = _init_functions();
    if (!selected || selected.indexOf("All Algorithms") != -1)
        for (var i = 0; i < functions.length; i++) {
            var function_data = functions[i]['function_data'];
            var name_algorithm = functions[i]['name_algorithm'];
            newContainer(i)
            var container = "container" + i;
            _get_data(function_data, name_algorithm, container)
        }
    else {
        for (var i = 0; i < functions.length; i++) {
            for (var j = 0; j < selected.length; j++) {
                if (functions[i]['name_algorithm'] == selected[j]) {
                    var function_data = functions[i]['function_data'];
                    var name_algorithm = functions[i]['name_algorithm'];
                    newContainer(i)
                    var container = "container" + i;
                    _get_data(function_data, name_algorithm, container);
                    break;
                }
            }
        }
    }

}

function _init_events() {

    $('#refresh_data').click(function () {
        var a_data = $('#algorithms option:selected');
        var selected = [];
        $(a_data).each(function (index, data) {
            console.log(data)
            selected.push($(this).val());
        });
        $("#graphs").empty()
        charge_algorithm(selected);

        $('#graphs')[0].style.display = 'none';
        show_loading()
    });

    $('#refresh_data_configuration').click(function () {

        var dato_archivo = $('#formFile').prop("files")[0];
        var form_data = new FormData();
        form_data.append("file", dato_archivo);
        $.ajax({
            url: "main.php",
            dataType: 'json',
            processData: false,
            data: form_data,
            type: 'post',
            contentType: false,
            mimeType: "multipart/form-data",
            success: function (response) {

                $('#formFile').val('')
                $("#graphs").empty()
                var i = 0
                response.forEach(function (element) {
                    var algorithm = element[2]["name_algorithm"];
                    element.pop()
                    newContainer(i)
                    var container = "container" + i;
                    $('#graph' + i)[0].style.display = '';
                    _init_graph(element, container, algorithm);
                    i = i + 1
                });


            },
            error: function () {
                alert("Ha ocurrido un error");
            }
        });
    });


}

function _init_fields() {
    var data = {"function": "show_fields"};
    $.ajax({
        url: "main.php",
        type: "GET",
        data: data,
        dataType: "json",
        submit: "true",
        success: function (response) {
            console.log(response)
            var sel = document.getElementById('algorithms');
            var tamano_array = response['name_algorithms']['data'].length
            for (var i = 0; i < tamano_array; i++) {
                var opt = document.createElement('option');
                if (i > -1) {
                    opt.innerHTML = response['name_algorithms']['data'][i]['value'];
                    opt.value = response['name_algorithms']['data'][i]['value'];
                    if (i == 0)
                        opt.selected = true;
                    sel.appendChild(opt);

                }
            }

            var sel = document.getElementById('dataset');
            var tamano_array = response['dataset']['data'].length
            for (var i = 0; i < tamano_array; i++) {
                var opt = document.createElement('option');
                if (i > -1) {
                    opt.innerHTML = response['dataset']['data'][i]['value'];
                    opt.value = response['dataset']['data'][i]['value'];
                    if (i == 0)
                        opt.selected = true;
                    sel.appendChild(opt);

                }
            }


            days_prediction = ["200", "250", "300", "350", "400"];
            var sel = document.getElementById('days_prediction');
            days_prediction.forEach(function (item, index) {
                var opt = document.createElement('option');
                opt.innerHTML = item;
                opt.value = item;
                sel.appendChild(opt);
            })

            charge_algorithm();

            console.log(response);
        }
    });
}

function _get_data(function_data, name_algorithm, container) {
    var date = $('#date_picker').val();
    var days_prediction = $('#days_prediction').val();
    var data = {
        "function": function_data,
        "date": date,
        "days_prediction": days_prediction
    };
    console.log(data);

    $.ajax({
        url: "main.php",
        type: "GET",
        data: data,
        dataType: "json",
        submit: "true",
        success: function (response) {
            console.log(response);
            var graphs = $('#graphs')[0];
            var no_data = $('#no_data')[0];
            if (!response) {
                graphs.style.display = 'none';
                no_data.style.display = '';
                return false;
            } else {
                graphs.style.display = '';
                no_data.style.display = 'none';
                _init_graph(response, container, name_algorithm);
            }
            hide_loading()

        }
    });
}

function _init_date_picker() {


    var urlParams = new URLSearchParams(window.location.search);
    var date = urlParams.get('date');
    if (date) {
        d_init_date_picker();
        date = date.split(" - ");
        date = date[0];
    } else {
        date = moment().subtract(4, 'months')
    }


    $("#date_picker").daterangepicker({
        "showWeekNumbers": true,
        "startDate": date,
        "locale": {
            "format": 'YYYY-MM-DD',
            "firstDay": 1
        },
        "singleDatePicker": true
    });


}

function hide_loading() {
    var loading = document.getElementsByClassName("loading")[0]
    if (loading.style.display == "")
        loading.style.display = "none"
}

function show_loading() {
    var loading = document.getElementsByClassName("loading")[0]
    console.log(loading.style.display)
    if (loading.style.display == "none")
        loading.style.display = ""
}

function _init_graph(data, name_container, name) {

    Highcharts.chart(name_container, {

        title: {
            text: name
        },

        yAxis: {
            title: {
                text: 'Value'
            }
        },

        tooltip: {
            // enabled: true,
            // followTouchMove: false,
            crosshairs: true,
            shared: true,
            followPointer: true,
            borderWidth: 0,
            style: {
                color: '#966a6c'
            },
        },

        series: data,

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });
}


function add_column() {
    var id = document.getElementsByClassName("column_lavel").length + 1

    var new_html = "<div class=\"row\" id='column_" + id + "'>\n" +
        "                    <div class=\"col-lg-2 col-md-6 col-sm-6 col-6 m-b\">\n" +
        "                        <label class='column_lavel' id='" + id + "'>Column " + id + "</label>\n" +
        "                        <select class=\"form-control chosen\" id = \"sel_column_" + id + "\" data-placeholder=\"Choose an option please\">\n" +
        "                        </select>\n" +
        "                    </div>\n" +
        "                    <div class=\"col-lg-2 col-md-6 col-sm-6 col-6 m-b\" style=\"padding-left: 0px\">\n" +
        "                        <button type=\"button\" class=\"btn btn-info button_delete_" + id + "\" onclick=delete_column(this.id) id='" + id + "' style=\"margin-top: 27px; background-color: red;border-color: red\">-</button>\n" +
        "                    </div>\n" +
        "                </div>"
    var more_config = document.getElementById("more_config")
    more_config.innerHTML = more_config.innerHTML + new_html
    fillConfig(id)


}

function orderColumns() {
    var columns = document.getElementsByClassName("column_lavel")
    for (var i = 0; i < columns.length; i++) {
        var last_id = columns[i].id
        var div_row = document.getElementById("column_" + last_id)
        var button_delete = document.getElementsByClassName("button_delete_" + last_id)[0]
        var sel_column = document.getElementById("sel_column_" + last_id)
        if (i > 0) {
            div_row.id = "column_" + (i + 1)
            button_delete.className = "btn btn-info button_delete_" + (i + 1)
            button_delete.id = (i + 1)
            sel_column.id = "sel_column_" + (i + 1)
        }
        columns[i].innerHTML = "Column " + (i + 1)
        columns[i].id = (i + 1)
    }
}

function delete_column(id_delete) {
    document.getElementById("column_" + id_delete).remove();
    orderColumns()
}

function fillConfig(id) {
    var array = ["Algorithm", "Date", "Y axis"]
    var sel = document.getElementById('sel_column_' + id);
    var tamano_array = array.length
    for (var i = 0; i < tamano_array; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = array[i];
        opt.value = array[i];
        sel.appendChild(opt);
    }
}

function newContainer(index) {

    var html = "<div class=\"col-lg-6\" id=\"graph" + index + "\">\n" +
        "            <div class=\"ibox-content\" style=\"margin-top: 20px;\">\n" +
        "                <div class=\"highcharts-figure\">\n" +
        "                    <div id=\"container" + index + "\"></div>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </div>"

    $("#graphs").append(html);

}


$('#show_config').click(function () {
    var config_optional = document.getElementsByClassName("config_optional")[0]
    var show_config = document.getElementById("show_config")

    if (config_optional.style.display == "none") {
        config_optional.style.display = ""
        show_config.textContent = "Hide configuration options"
    } else {
        config_optional.style.display = "none"
        show_config.textContent = "Show configuration options"
    }
});


main();
