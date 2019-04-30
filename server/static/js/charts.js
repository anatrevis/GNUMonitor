var objects_chart_list = [];

if (list_charts_pk.length > 0){
  for (var j=0; j<list_charts_pk.length; j++) {
    var chart_div_id = list_charts_pk[j];
    var chart_title = list_charts_title[j];
    var charts_xAxis_name = list_charts_xAxis_name[j];
    var charts_yAxis_name = list_charts_yAxis_name[j];
    objects_chart_list[j]= Highcharts.chart({
        chart: {
            renderTo: String(chart_div_id),
            type: 'line'
        },

        credits: {
          enabled: false
        },

        title: {
            text: String(chart_title)
        },



        yAxis: {
          title: {
              text: String(charts_yAxis_name)
          }
        },

        xAxis: {
          type:'datetime',
          // dateTimeLabelFormats: {
          //    day: '%e of %b'
          // },
          // categories: [{% for data in monidata %}'{{ data.time.time }}' {% if not forloop.last %}, {% endif %}{% endfor %}],
          title: {
             text: String(charts_xAxis_name)
           },
        },

        plotOptions: {
          line: {
              // dataLabels: {
              //     enabled: true
              // },
              enableMouseTracking: true
          }
        },

        series: [{
          name: String(charts_yAxis_name)
          // data: [
          //   {% for data in monidata %}{{ data.value  }}{% if not forloop.last %}, {% endif %}{% endfor %}
          // ],

      }]

    });
  };
};
