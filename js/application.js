const baseUrl = 'https://fastapiallocine.herokuapp.com/api/v2/';
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
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                title: {
                    text: "Mois de sortie"
                }
            },
            series: [{
                name: "Nombre de sortie",
                data: saisonality,
                showInLegend: false
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
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Distribution des filmes selon leur genre'
            },
            subtitle: {
                text: 'Source: allocine.fr'
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
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                data: genre
                }]
        });
    }
);
