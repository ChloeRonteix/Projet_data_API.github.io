const baseUrl = 'http://127.0.0.1:8000/api/v2/';
//const baseUrl = 'http://127.0.0.1:5000/api/v1/';//

Highcharts.getJSON(baseUrl+'films/month',
    function (data) {
        const saisonality = data.filter(d => !!d.month).map(d => [d.month-1, d.number_of_films]);

        Highcharts.chart('graph1', {

            title: {
                text: 'Saisonnalité des sorties de films'
            },
        
            subtitle: {
                text: 'Source: allocine.fr'
            },
        
            yAxis: {
                title: {
                    text: 'Sorties de films'
                }
            },
        
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
        
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            series: [{
                data: saisonality
            }],
        
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
);

Highcharts.getJSON(baseUrl+'films/genres',
    function (data) {
        const genre = data.sort((a,b) => b.number_of_films - a.number_of_films).map(d => [d.genre, d.number_of_films]);

        Highcharts.chart('graph2', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: 0,
                plotShadow: false
            },
            title: {
                text: 'Distribution des films par genre',
                align: 'center',
                verticalAlign: 'middle',
                y: 300
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        distance: -50,
                        style: {
                            fontWeight: 'bold',
                            color: 'white'
                        }
                    },
                    startAngle: 0,
                    endAngle: 360,
                    center: ['50%', '75%'],
                    size: '100%'
                }
            },
            series: [{
                type: 'pie',
                name: 'genre share',
                innerSize: '50%',
                data: genre
            }]
        });
    }
);

