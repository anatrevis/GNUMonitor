var objects_chart_list = [];

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

function Host_Monitor_Chart() {
    /**
   * Create a constructor for sparklines that takes some sensible defaults and merges in the individual
   * chart options. This function is also available from the jQuery plugin as $(element).highcharts('SparkLine').
   */
  Highcharts.SparkLine = function (a, b, c) {
      var hasRenderToArg = typeof a === 'string' || a.nodeName,
          options = arguments[hasRenderToArg ? 1 : 0],
          defaultOptions = {
              chart: {
                  renderTo: (options.chart && options.chart.renderTo) || this,
                  backgroundColor: null,
                  borderWidth: 0,
                  type: 'area',
                  margin: [2, 0, 2, 0],
                  width: 90,
                  height: 50,
                  style: {
                      overflow: 'visible'
                  },

                  // small optimalization, saves 1-2 ms each sparkline
                  skipClone: true
              },
              title: {
                  text: ''
              },
              credits: {
                  enabled: false
              },
              exporting: {
                enabled: false
              },
              xAxis: {
                  labels: {
                      enabled: false
                  },
                  title: {
                      text: null
                  },
                  startOnTick: false,
                  endOnTick: false,
                  tickPositions: []
              },
              yAxis: {
                  endOnTick: false,
                  startOnTick: false,
                  labels: {
                      enabled: false
                  },
                  title: {
                      text: null
                  },
                  tickPositions: [0]
              },
              legend: {
                  enabled: false
              },
              tooltip: {
                  hideDelay: 0,
                  outside: true,
                  shared: true
              },
              plotOptions: {
                  series: {
                      animation: false,
                      lineWidth: 1,
                      shadow: false,
                      states: {
                          hover: {
                              lineWidth: 1
                          }
                      },
                      marker: {
                          radius: 1,
                          states: {
                              hover: {
                                  radius: 2
                              }
                          }
                      },
                      fillOpacity: 0.25
                  },
                  column: {
                      negativeColor: '#910000',
                      borderColor: 'silver'
                  }
              }
          };

      options = Highcharts.merge(defaultOptions, options);

      return hasRenderToArg ?
          new Highcharts.Chart(a, options, c) :
          new Highcharts.Chart(options, b);
  };

  var start = +new Date(),
      $tds = $('td[data-sparkline]'),
      fullLen = $tds.length,
      n = 0;

  // Creating 153 sparkline charts is quite fast in modern browsers, but IE8 and mobile
  // can take some seconds, so we split the input into chunks and apply them in timeouts
  // in order avoid locking up the browser process and allow interaction.
  function doChunk() {
      var time = +new Date(),
          i,
          len = $tds.length,
          $td,
          stringdata,
          arr,
          data,
          chart;

      for (i = 0; i < len; i += 1) {
          $td = $($tds[i]);
          stringdata = $td.data('sparkline');
          arr = stringdata.split('; ');
          data = $.map(arr[0].split(', '), parseFloat);
          chart = {};

          if (arr[1]) {
              chart.type = arr[1];
          }
          $td.highcharts('SparkLine', {
              series: [{
                  data: data,
                  pointStart: 1
              }],
              tooltip: {
                  headerFormat: '<span style="font-size: 10px">' + $td.parent().find('th').html() + ', Q{point.x}:</span><br/>',
                  pointFormat: '<b>{point.y}.000</b> USD'
              },
              chart: chart
          });

          n += 1;

          // If the process takes too much time, run a timeout to allow interaction with the browser
          if (new Date() - time > 500) {
              $tds.splice(0, i + 1);
              setTimeout(doChunk, 0);
              break;
          }
          // Print a feedback on the performance
      }
  }
  doChunk();
};
