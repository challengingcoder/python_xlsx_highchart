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
        $('#customization-form').submit();
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

        var chartObj = null;
        if (chartType === CHART_TYPE_BAR) {
            chartObj = chartObjBar(title, categories, series, 'bar');
        } else if (chartType === CHART_TYPE_COLUMN) {
            chartObj = chartObjBar(title, categories, series, 'column');
        } else if (chartType === CHART_TYPE_LINE) {
            chartObj = chartObjBar(title, categories, series, 'line');
        } else if (chartType === CHART_TYPE_PIE) {
            chartObj = chartObjBarPie(title, categories, series);
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

var chartObjBarPie = function (title, categories, seriesData) {
    var colors = Highcharts.getOptions().colors,
        data = [],
        innerCategories = [],
        i = 0,
        c = 0;

    for (i = 0; i < seriesData.length; i++) {

        innerCategories.push(seriesData[i].name);

        var color = colors[i],
            sum = 0;

        for (c = 0; c < seriesData[i].data.length; c++) {
            sum += seriesData[i].data[c]
        }

        data.push(
            {
                y: sum,
                color: color,
                drilldown: {
                    name: seriesData[i].name + ' Vars',
                    categories: categories,
                    data: seriesData[i].data,
                    color: colors[0]
                }
            }
        )
    }


    var dataLen = data.length,
        innerData = [],
        outherData = [],
        drillDataLen,
        brightness;


    for (i = 0; i < dataLen; i += 1) {
        innerData.push({
            name: innerCategories[i],
            y: data[i].y,
            color: data[i].color
        });

        drillDataLen = data[i].drilldown.data.length;
        for (j = 0; j < drillDataLen; j += 1) {
            brightness = 0.2 - (j / drillDataLen) / 5;
            outherData.push({
                name: data[i].drilldown.categories[j],
                y: data[i].drilldown.data[j],
                color: Highcharts.Color(data[i].color).brighten(brightness).get()
            });
        }
    }

    return {
        chart: {
            type: 'pie'
        },
        title: {
            text: title
        },

        yAxis: {
            title: {
                text: null
            }
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },
        tooltip: {
            enabled: false
        },
        series: [{
            data: innerData,
            size: '50%',
            dataLabels: {
                formatter: function () {
                    return this.point.name
                },
                color: '#ffffff',
                distance: -80
            },
            id: 'inner'
        }, {
            data: outherData,
            size: '80%',
            innerSize: '50%',
            dataLabels: {
                formatter: function () {
                    // display only if larger than 1
                    return this.y > 1 ? '<b>' + this.point.name + ':</b> ' +
                        this.y + '%' : null;
                }
            },
            id: 'outher'
        }],
        credits: {
            enabled: false
        }
    }
};