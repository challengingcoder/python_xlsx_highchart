$(function () {
    $('.slide-list li').click(function () {
        var i = $(this).data('index');
        window.location.href = '/builder/' + i;
    });

    $('.input-cross-break, .input-chart-type').change(function () {
        $('.btn-save').prop('disabled', false);
    });
});


$(function () {
    $.getJSON('?json=1', function (resp) {
        if (chartType === 1) {
            var chartObj = chartObjBar(resp.question, resp.options, resp.sections[crossBreakIndex].categories);
            Highcharts.chart('chart-container', chartObj);
        }
    });
});


var chartObjBar = function (title, categories, seriesData) {
    var chartObj = {
        chart: {
            type: 'bar'
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
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
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