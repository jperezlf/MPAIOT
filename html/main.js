function main() {
    _init_date_picker();
    _init_fields();
    _init_events();


    console.log("Iniciando renderizado")
}


function _init_functions() {

    return [
        {"function_data": "get_data_xgboost", "name_algorithm": "XGBoost"},
        {"function_data": "get_data_linregmult", "name_algorithm": "Linear Regression Múltiple"},
        {"function_data": "get_data_linregmultstastmodel", "name_algorithm": "Linear Regression Múltiple Stats Model"},
        {"function_data": "get_data_randomforest", "name_algorithm": "Ramdom Forest"},
        {"function_data": "get_data_svr", "name_algorithm": "Support Vector Regression"},
        {"function_data": "get_data_logisticregression", "name_algorithm": "Logistic Regression"},
        {"function_data": "get_data_stochasticgradientdescent", "name_algorithm": "Stochastic Gradient Descent"},
        {"function_data": "get_data_bart", "name_algorithm": "Bayesian Additive Regressions Trees"},
        {"function_data": "get_data_gaussiannaivebayes", "name_algorithm": "Gaussian Naive Bayes"},
        {"function_data": "get_data_isotonicregression", "name_algorithm": "Isotonic Regression"},
        {"function_data": "get_data_earth", "name_algorithm": "eARTH"},
    ]
}

function charge_algorithm(selected) {
    var functions = _init_functions();
    if (!selected || selected.indexOf("All Algorithms") != -1)
        for (var i = 0; i < functions.length; i++) {
            var function_data = functions[i]['function_data'];
            var name_algorithm = functions[i]['name_algorithm'];
            var container = "container" + i;
            _get_data(function_data, name_algorithm, container)
            $('#graph' + i)[0].style.display = '';
        }
    else {
        for (var i = 0; i < functions.length; i++) {
            var enc = false;
            for (var j = 0; j < selected.length; j++) {
                if (functions[i]['name_algorithm'] == selected[j]) {
                    var function_data = functions[i]['function_data'];
                    var name_algorithm = functions[i]['name_algorithm'];
                    var container = "container" + i;
                    $('#graph' + i)[0].style.display = '';
                    _get_data(function_data, name_algorithm, container);
                    enc = true
                    break;
                }
            }
            if (!enc)
                $('#graph' + i)[0].style.display = 'none';
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
        charge_algorithm(selected);

        $('#graphs')[0].style.display = 'none';
        show_loading()
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
            var sel = document.getElementById('series');
            var tamano_array = response['name_series']['data'].length
            for (var i = 0; i < tamano_array; i++) {
                var opt = document.createElement('option');
                if (i > 0) {
                    opt.innerHTML = response['name_series']['data'][i]['value'];
                    opt.value = response['name_series']['data'][i]['value'];
                    sel.appendChild(opt);

                }
            }
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
    var series_name = $('#series').val();
    var date = $('#date_picker').val();
    var days_prediction = $('#days_prediction').val();
    var data = {
        "function": function_data,
        "series_name": series_name,
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

    //data = moldear_array(data);

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

main();
