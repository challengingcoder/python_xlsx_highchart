var CHART_TYPE_BAR = 1;
var CHART_TYPE_COLUMN = 2;
var CHART_TYPE_LINE = 3;
var CHART_TYPE_PIE = 4;

var SERIES_BY_CATEGORIES = 1;
var SERIES_BY_OPTIONS = 2;


$(function () {
    $('.slide-list li').click(function () {
        var i = $(this).data('index');
        window.location.href = '/builder/' + i;
    });

    $('.input-cross-break, .input-chart-type, .input-series').change(function () {
        $('.btn-save').prop('disabled', false);
    });
});


$(function () {
    $.getJSON('?json=1', function (resp) {

        var title = resp.question;
        var categories = resp.options;
        var series = resp.sections[crossBreakIndex].categories;

        if (seriesBy === SERIES_BY_OPTIONS) {

            var newCategories = [];
            for (var i = 0; i < series.length; i++) {
                newCategories.push(series[i]['name']);
            }

            categories = newCategories;
            series = resp.data_by_options[crossBreakIndex];
        }

        console.log(categories);
        console.log(series)

        var chartObj = null;
        if (chartType === CHART_TYPE_BAR) {
            chartObj = chartObjBar(title, categories, series, 'bar');
        } else if (chartType === CHART_TYPE_COLUMN) {
            chartObj = chartObjBar(title, categories, series, 'column');
        } else if (chartType === CHART_TYPE_LINE) {
            chartObj = chartObjBar(title, categories, series, 'line');
        } else if (chartType === CHART_TYPE_PIE) {

        }

        if (chartObj !== null) {
            Highcharts.chart('chart-container', chartObj);
        }

    });
});


var chartObjBar = function (title, categories, seriesData, type) {


    var chartObj = {
        chart: {
            type: type
        },
        title: {
            text: title
        },
        xAxis: {
            categories: categories,
            title: {
                text: null
            }
        },
        yAxis: {
            title: {
                text: null
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true,
                    format: "{y}%"
                }
            },
            line: {
                dataLabels: {
                    enabled: true,
                    format: "{y}%"
                }
            },
            column: {
                dataLabels: {
                    enabled: true,
                    format: "{y}%"
                }
            }
        },
        legend: {
            enabled: true

        },
        credits: {
            enabled: false
        },
        series: seriesData
    };

    return chartObj
};