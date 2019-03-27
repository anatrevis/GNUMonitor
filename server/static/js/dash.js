var cont = chart1.series[0].data.length;
var throughput_array = [];
var data_list = [];
var id_last_item = 0;

function console_print_chart_data(){
  // console.log("This is the chart data: " + JSON.stringify(chart1.series[0].data));
  for (var i=0; i<chart1.series[0].data.length; i++){
    console.log(chart1.series[0].data[i]['throughput']);
  }
};

$( "#5points" ).click(function() {
    console_print_chart_data();
    console.log(cont);
    if (cont > 5){
      cont = 5;
      clearChartlData(cont);
    }
});

$( "#10points" ).click(function() {
    console_print_chart_data();
    console.log(cont);
    if (cont > 10){
      cont = 10;
      clearChartlData(cont);
    }
});

$( "#20points" ).click(function() {
    console_print_chart_data();
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


setInterval(function (){
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

          plot_chart1(data_list);

          console.log(data_list);
          console.log(id_last_item);



      },
      failure: function(data) {
          console.log("hello")
          alert('Got an error dude');
      }
    });
  }, 1000);


  function plot_chart1(chart1_data){
    for (var i = 0; i < chart1_data.length; i++){
      chart1.series[0].addPoint(chart1_data[i]['throughput'])
    }

  }
