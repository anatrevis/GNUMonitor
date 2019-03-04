// 
// Highcharts.chart('chart', {
//       chart: {
//           type: 'line'
//       },
//
//       credits: {
//         enabled: false
//       },
//
//       title: {
//           text: 'Monitor Data'
//       },
//
//       yAxis: {
//         title: {
//             text: 'Throughput'
//         }
//       },
//
//       xAxis: {
//         categories: [{% for data in monidata %}'{{ data.time }}' {% if not forloop.last %}, {% endif %}{% endfor %}],
//         title: {
//            text: 'Time'
//          },
//       },
//
//       plotOptions: {
//         line: {
//             dataLabels: {
//                 enabled: true
//             },
//             enableMouseTracking: false
//         }
//       },
//
//       series: [{
//         name: 'Throughput',
//         data: [
//           {% for data in monidata %}{{ data.throughput  }}{% if not forloop.last %}, {% endif %}{% endfor %}
//         ],
//
//     }]
//   });
