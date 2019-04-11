var cont = 0;
var throughput_array = [];
var data_list = [];
var id_last_item = 0;

function console_print_chart_data(){
  // console.log("This is the chart data: " + JSON.stringify(chart1.series[0].data));
  for (var i=0; i<chart1.series[0].data.length; i++){
    console.log(chart1.series[0].data[i]['y']);
  }
};

$( "#5points" ).click(function() {
    console_print_chart_data();
    cont = chart1.series[0].data.length;
    console.log(cont);
    if (cont > 5){
      cont = 5;
      clearChartlData(cont);
    }
});

$( "#10points" ).click(function() {
    console_print_chart_data();
    cont = chart1.series[0].data.length;
    console.log(cont);
    if (cont > 10){
      cont = 10;
      clearChartlData(cont);
    }
});

$( "#20points" ).click(function() {
    console_print_chart_data();
    cont = chart1.series[0].data.length;
    console.log(cont);
    if (cont > 20){
      cont = 20;
      clearChartlData(cont);
    }
});

function clearChartlData(cont){
  console.log("clearing chart data!");
  while(chart1.series[0].data.length > cont){
    console.log("clearing");
    chart1.series[0].data[0].remove();
  }
  console_print_chart_data();
  console.log("ready!");
};


function postCharts(){
  console.log("Data!");
  $.ajax({
      url: "/gnumonitor/rest",
      type: 'GET',
      dataType: 'json',
      data: {id_last_item: id_last_item},
      success: function(data) {

          data_list = data;

          if (data.length > 0){
            id_last_item = data_list[(data.length) - 1]['id'];
          }

          //console.log(list_charts.length);

          for (i=0; i<objects_chart_list.length;i++){
            //var id_chart = list_charts[i];
            var chart_data = data_list.filter(function(p){return p.id_chart_id == list_charts_pk[i];});
            console.log(chart_data);
            console.log(list_charts_pk[i]);
            plot_chart(chart_data, objects_chart_list[i]);
          }
          //plot_chart1(data_list);
          //
          // for char in list_chart:
          //   id = chart.id;
          //   list_data = data_list.filter(function(p){return p.id_chart_id == id;});

          console.log(id_last_item);
          //console.log(list_charts);



      },
      failure: function(data) {
          console.log("hello")
          alert('Got an error dude');
      }
    });
};


function plot_chart(chart_data, object_chart){
  for (var i = 0; i < chart_data.length; i++){
    //var x = chart1_data[i]['time'];
    //var x = new Date(chart1_data[i]['time']).getTime();
    //fist_unix_date = chart1_data[0]['time'];
    var x = new Date(chart_data[i]['time']).getTime();
    var y = chart_data[i]['value'];
    object_chart.series[0].addPoint([x, y]);
  }
};




$(document).ready(function(){
  postCharts();
  // var btn = $('submit_button');
  // $('submit_button').click(function(){
  //     modal('hide');
  // }
  // setInterval(function (){
  //   postChart1();
  // }, 1000);
});
