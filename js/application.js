const baseUrl = 'http://127.0.0.1:5000/api/v1/';

Highcharts.getJSON(baseUrl+'films/month',
    function (data) {
        const saisonality = data.filter(d => !!d.month).map(d => [d.month-1, d.number_of_films]);

        Highcharts.chart('container', {

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



