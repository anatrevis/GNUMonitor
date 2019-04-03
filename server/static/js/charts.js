var chart1 = Highcharts.chart('chart1', {
    chart: {
        type: 'line'
    },

    credits: {
      enabled: false
    },

    title: {
        text: 'Monitor Data'
    },

    yAxis: {
      title: {
          text: 'Throughput'
      }
    },

    xAxis: {
      type:'datetime',
      // dateTimeLabelFormats: {
      //    day: '%e of %b'
      // },
      //categories: [{% for data in monidata %}'{{ data.time.time }}' {% if not forloop.last %}, {% endif %}{% endfor %}],
      title: {
         text: 'Time'
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
      name: 'Throughput',
      data: [
        //{% for data in monidata %}{{ data.throughput  }}{% if not forloop.last %}, {% endif %}{% endfor %}
      ],

  }]

});
