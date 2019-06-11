var objects_chart_list = [];
var objects_host_CPU_list = [];
var objects_host_RAM_list = [];
var objects_host_DISK_list = [];

function Monitor_Chart(){
  if (list_charts_pk.length > 0){
    for (var j=0; j<list_charts_pk.length; j++) {
      var chart_div_id = list_charts_pk[j];
      var chart_title = list_charts_title[j];
      var charts_xAxis_name = list_charts_xAxis_name[j];
      var charts_yAxis_name = list_charts_yAxis_name[j];
      objects_chart_list[j]= Highcharts.chart({
          chart: {
              renderTo: String('chart_'+chart_div_id),
              type: 'line',
              // height: 200,
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
};



function Host_Monitor_Chart(){

  console.log("PLOTADO");
  if (list_hosts_pk.length > 0){
    for (var b=0; b<list_hosts_pk.length; b++) {
      var div_id = list_hosts_pk[b];

      objects_host_CPU_list[b]= Highcharts.chart({
      chart: {
          backgroundColor: '#eee',
          renderTo: String('CPU_'+div_id),
          borderWidth: 0,
          type: 'area',
          height: 70,
          margin: [0, 0, 0, 0],
          style: {
            overflow: 'visible'
          },

      },
      legend: {
        enabled: false,
      },
      title: {
          text: ''
      },
      subtitle: {
          text: ''
      },
      exporting: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      xAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        startOnTick: false,
        endOnTick: false,
        tickPositions: []
      },
      yAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        gridLineWidth: 0,
        endOnTick: false,
        startOnTick: false,
        tickPositions: [0],
        min: 0,
        max: 110,
      },
      tooltip: {
        hideDelay: 0,
        outside: true,
        shared: true
      },
      plotOptions: {
          area: {
              pointStart: 1940,
              marker: {
                  enabled: false
              }
          }
      },
      series: [{
          name: '',
      },]
    });

      objects_host_RAM_list[b]=Highcharts.chart({
      chart: {
          backgroundColor: '#eee',
          renderTo: String('RAM_'+div_id),
          borderWidth: 0,
          type: 'area',
          height: 70,
          margin: [0, 0, 0, 0],
          style: {
            overflow: 'visible'
          },

      },
      legend: {
        enabled: false,
      },
      title: {
          text: ''
      },
      subtitle: {
          text: ''
      },
      exporting: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      xAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        startOnTick: false,
        endOnTick: false,
        tickPositions: []
      },
      yAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        gridLineWidth: 0,
        endOnTick: false,
        startOnTick: false,
        tickPositions: [0],
        min: 0,
        max: 110,
      },
      tooltip: {
        hideDelay: 0,
        outside: true,
        shared: true
      },
      plotOptions: {
          area: {
              pointStart: 1940,
              marker: {
                  enabled: false
              }
          }
      },
      series: [{
          name: '',
      },]
    });

      objects_host_DISK_list[b]=Highcharts.chart({
      chart: {
          backgroundColor: '#eee',
          renderTo:('DISK_'+div_id),
          borderWidth: 0,
          type: 'area',
          height: 70,
          margin: [0, 0, 0, 0],
          style: {
            overflow: 'visible'
          },

      },
      legend: {
        enabled: false,
      },
      title: {
          text: ''
      },
      subtitle: {
          text: ''
      },
      exporting: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      xAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        startOnTick: false,
        endOnTick: false,
        tickPositions: []
      },
      yAxis: {
        title: {
            enabled: false
        },
        labels: {
            enabled: false
        },
        tickLength: 0,
        gridLineWidth: 0,
        endOnTick: false,
        startOnTick: false,
        tickPositions: [0],
        min: 0,
        max: 110,
      },
      tooltip: {
        hideDelay: 0,
        outside: true,
        shared: true
      },
      plotOptions: {
          area: {
              pointStart: 1940,
              marker: {
                  enabled: false
              }
          }
      },
      series: [{
          name: '',
      },]
    });
    }

  };

  //console.log("CRIEI a objects_host_CPU_list");
  //console.log(objects_host_CPU_list);
};
