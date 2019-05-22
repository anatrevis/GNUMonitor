var cont = 0;
var data_list = [];
var id_last_item = 0;
var id_last_error = 0;

$(function(){
    $(".heading-compose").click(function() {
      $(".side-two").css({
        "left": "0"
      });
    });

    $(".newMessage-back").click(function() {
      $(".side-two").css({
        "left": "-100%"
      });
    });
})


function System_Errors() {
  $.ajax({
      url: "/gnumonitor/create_errors_list/",
      type: 'GET',
      dataType: 'json',
      // data: {id_last_error: id_last_error},
      success: function(errors) {
          errorslist = errors;
          console.log(errorslist);
          var enable_btn = errorslist.filter(function(p){return p.description == "Warning: No client connection";});
          //console.log(enable_btn);
          if (enable_btn !== 'undefined' && enable_btn.length == 0){
            //console.log("TEM CONEXAO COM O CLIENTE");
            $("#add_monitoring").removeClass("nav-link disabled").addClass("nav-link");

          }

          if (errorslist.length > 0){
            if(!$("#errors_div").length){
                $("#body_base").prepend("<div id='errors_div'></div>");
                // $("#notifications").prepend("<div class='col' id='errors_div'></div>");
            }

            var new_ids = [];
            //ADD NEW ERRORS
            for (i=0; i<errorslist.length;i++){
            //for (var error in errorslist ) {
              //console.log(errorslist[i]['id']);
              new_ids.push(errorslist[i]['id']);
              if(!$('#'+errorslist[i]['id']).length){
                //console.log("Nao Existe");
                //$("#errors_reports").append("<p id="+errorslist[i]['id']+" >"+errorslist[i]['chart_object_id']+" "+errorslist[i]['description']+"</p>");
                if(errorslist[i]['type']=="Error"){
                  $("#errors_div").append("<div class='alert alert-danger' role='alert' id="+errorslist[i]['id']+" >"+errorslist[i]['description']+"</div>");
                }

                else{
                  $("#errors_div").append("<div class='alert alert-warning' role='alert' id="+errorslist[i]['id']+" >"+errorslist[i]['description']+"</div>");
                }

              }
            }
            //REMOVE SOLVED ERRORS
            var old_ids = [];
            var solved_errors = [];

            $("#errors_div").find("div").each(function(){
              if(this.id>0){
                old_ids.push(this.id);
                console.log('ID:' +this.id);
                var contem = 0;
                for (i=0; i<new_ids.length;i++){//se new_ids nao contem this.id entao faz
                  //console.log("compara: "+new_ids[i]+ " com"+this.id);
                  if (parseInt(new_ids[i]) == parseInt(this.id)){
                    //console.log("deu igual")
                    contem = 1;
                    break;
                  }
                }
                if(contem == 0){
                  //console.log("deu DIFERENTE "+ this.id)
                  $('#'+this.id).remove();
                  solved_errors.push(this.id)
                }
              }
            });
            //console.log('Old:' +old_ids);
            //console.log('New:' +new_ids);
            //console.log('Solved:' +solved_errors);




          } else {
            if($("#errors_div").length){
                $("#errors_div").remove();
            }
          }

      },
      failure: function(errors) {
          alert('Got an error dude');
      }
    });
};

function Destroy_Chart() {
  var btn = (event.target);
  var raw_chart_pk_to_destroy = btn.id;
  var chart_pk_to_destroy = raw_chart_pk_to_destroy.split("_")[2];
  console.log(chart_pk_to_destroy);
  $.ajax({
       url:'/gnumonitor/delete_chart/',
       type: 'GET',
       data: {chart_pk_to_destroy: chart_pk_to_destroy},
       success: function() {
           console.log(chart_pk_to_destroy);
           for (i=0; i<list_charts_pk.length;i++){
             console.log(list_charts_pk[i]);
             console.log(chart_pk_to_destroy);
             if (list_charts_pk[i] == chart_pk_to_destroy){
               list_charts_pk.splice(i, 1);
               list_charts_title.splice(i, 1);
               list_charts_xAxis_name.splice(i, 1);
               list_charts_yAxis_name.splice(i, 1);
               objects_chart_list.splice(i, 1);
             }
           }
       },
       failure: function(data) {
           alert('Got an error dude');
       }
   });

   btn.parentElement.remove(btn);
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
          console.log(data);

          if (data_list.length > 0){
            id_last_item = data_list[(data_list.length) - 1]['id'];
          }

          for (i=0; i<objects_chart_list.length;i++){
             var chart_data = data_list.filter(function(p){return p.chart_object_id == list_charts_pk[i];});
             // console.log(chart_data);
             // console.log(list_charts_pk[i]);
             plot_chart(chart_data, objects_chart_list[i]);
           }

          // console.log(id_last_item);
      },
      failure: function(data) {
          alert('Got an error dude');
      }
    });
};

function plot_chart(chart_data, object_chart){

  for (var i = 0; i < chart_data.length; i++){
    //Controle do last id pra nao bugar o monitoramento
    console.log(chart_data[i]['value']);
    if (id_last_item < chart_data[i]['id']){
      id_last_item = chart_data[i]['id'];
    }

    //console.log("im the OBJECT:"+object_chart);

    var shift = object_chart.series[0].data.length >= 60;
    //console.log("HERE:"+object_chart.series[0].data.length);

    //var x = chart1_data[i]['time'];
    //var x = new Date(chart1_data[i]['time']).getTime();
    //fist_unix_date = chart1_data[0]['time'];
    var x = new Date(chart_data[i]['time']).getTime();
    var y = chart_data[i]['value'];
    object_chart.series[0].addPoint([x, y], true, shift);
  };
};


function Clear_Chart(cont){
  console.log("clearing chart data!");
  var btn = (event.target);
  var raw_chart_pk_to_clean = btn.id;
  var chart_pk_to_clean = raw_chart_pk_to_clean.split("_")[2];
  console.log(chart_pk_to_clean);
  console.log(objects_chart_list);
  for (i=0; i<list_charts_pk.length;i++){
    console.log(list_charts_pk[i]);
    console.log(chart_pk_to_clean);

    if (list_charts_pk[i] == chart_pk_to_clean){
      object_chart_to_clear = objects_chart_list[i];
      console.log("ACHOU"+object_chart_to_clear);
      // for(i=0; i<object_chart_to_clear.series[0].data.length; i++){
      console.log(object_chart_to_clear.series[0].data.length);
      // object_chart_to_clear.series[0].remove();
      while(object_chart_to_clear.series[0].data.length > 0){
        object_chart_to_clear.series[0].data[0].remove();
      }
      break;
    }
  }
};
//
//   while(chart.series[0].data.length > cont){
//     console.log("clearing");
//     chart1.series[0].data[0].remove();
//   }
//   console.log("ready! Chart is clean");




$(document).ready(function(){
  setInterval(function (){
    // console.log("list:" + objects_chart_list);
    // console.log("length:" + objects_chart_list.length);
    if(objects_chart_list.length == 0){
      $( "#User_guide_1" ).show();
    }

    //console.log("errors:"+objects_errors_list)

    // if(objects_errors_list.length == 0){
    //    $( "#errors_div" ).hide();
    // }
    postCharts();
    System_Errors();
    // postErrors();

  }, 1000);
});

// function clearChartlData(cont){
//   console.log("clearing chart data!");
//   while(chart1.series[0].data.length > cont){
//     console.log("clearing");
//     chart1.series[0].data[0].remove();
//   }
//   console_print_chart_data();
//   console.log("ready!");
// };
// $( "#5points" ).click(function() {
//     console_print_chart_data();
//     cont = chart1.series[0].data.length;
//     console.log(cont);
//     if (cont > 5){
//       cont = 5;
//       clearChartlData(cont);
//     }
// });
//
// $( "#10points" ).click(function() {
//     console_print_chart_data();
//     cont = chart1.series[0].data.length;
//     console.log(cont);
//     if (cont > 10){
//       cont = 10;
//       clearChartlData(cont);
//     }
// });
//
// $( "#20points" ).click(function() {
//     console_print_chart_data();
//     cont = chart1.series[0].data.length;
//     console.log(cont);
//     if (cont > 20){
//       cont = 20;
//       clearChartlData(cont);
//     }
// });
//
// $( "#Clear" ).click(function() {
//
// });
// function console_print_chart_data(){
//   // console.log("This is the chart data: " + JSON.stringify(chart1.series[0].data));
//   for (var i=0; i<chart1.series[0].data.length; i++){
//     console.log(chart1.series[0].data[i]['y']);
//   }
// };
