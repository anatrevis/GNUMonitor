var cont = 0;
var data_list = [];
var id_last_item = 0;
var id_last_error = 0;
//Post_Hosts() variables
var objects_host_list= [];
var id_last_host = 0;
var list_hosts_pk= [];
var list_hosts_name = [];
var list_hosts_ip = [];
//Selected_Charts() variables
var id_last_chart = 0;
var id_selected_host =0;
var list_charts_pk = [];
var list_charts_title = [];
var list_charts_xAxis_name = [];
var list_charts_yAxis_name = [];
var selected_ids= [];

//var pk_selected_host = $( ".selected").attr('id');
//console.log("PK SELECTED HOST:"+ pk_selected_host);

function Post_Hosts(){ // Gets host informations, creates side bar cards for VM's connected
  // console.log("Hosts!");
  $.ajax({
      url: "/gnumonitor/hosts",
      type: 'GET',
      dataType: 'json',
      data: {id_last_host: id_last_host},
      success: function(hosts) {
      objects_host_list = hosts;
      // console.log('HOSTS:'+hosts);

      if (objects_host_list.length > 0){
        id_last_host = objects_host_list[(objects_host_list.length) - 1]['id'];
        // console.log(id_last_host);

        for (x=0; x<objects_host_list.length;x++){ //Create lists with hosts parameters
          list_hosts_pk.push(objects_host_list[x]['id']);
          list_hosts_name.push(objects_host_list[x]['name']);
          list_hosts_ip.push(objects_host_list[x]['ip']);

          $(".side_bar_cards_wrap").prepend("<div class='side_bar_card "+list_hosts_pk[x]+" sidecard' id="+list_hosts_pk[x]+"><div class='row' id="+list_hosts_pk[x]+"><div class='col' id="+list_hosts_pk[x]+"><p class='side_bar_card_title' id="+list_hosts_pk[x]+">"+list_hosts_name[x]+" ("+list_hosts_ip[x]+")</p></div><div class='col-xs'id="+list_hosts_pk[x]+"><p class='side_bar_card_last_time' id="+list_hosts_pk[x]+">16:32</p></div></div><div class='row' id="+list_hosts_pk[x]+"><table id='table-sparkline'><tbody id='tbody-sparkline'><tr><td class='label-sparkline' id="+list_hosts_pk[x]+">CPU</td><td data-sparkline='71, 78, 39, 66 '/><td class='label-sparkline' id="+list_hosts_pk[x]+">RAM</td><td data-sparkline='68, 52, 80, 96 '/><td class='label-sparkline'id="+list_hosts_pk[x]+" >DISK</td><td data-sparkline='3, 26, -41, -30'></tr></tbody></table></div></div>");
        }

        $("."+list_hosts_pk[0]+"").addClass("card_selected");//Fist VM start selected
        id_selected_host = list_hosts_pk[0];
        // console.log(id_selected_host);

        Host_Monitor_Chart();//Plots monitoring charts for VM's (CPU, RAM, DISK)
      }
  },
  failure: function(data) {
      alert('Error in Post_Hosts');
  }
  });
};

function Post_Charts(){ // Gets the registered charts informations
  // console.log("Charts!");
  $.ajax({
      url: "/gnumonitor/charts",
      type: 'GET',
      dataType: 'json',
      data: {id_selected_host: id_selected_host},
      success: function(charts) {

      // console.log('enviei este id: '+id_selected_host);

      selected_objects_chart_list = charts;
      // console.log(selected_objects_chart_list);

      if (selected_objects_chart_list.length > 0 && id_last_chart == 0){

        id_last_chart = selected_objects_chart_list[(selected_objects_chart_list.length) - 1]['id'];
        // console.log('ID Last chart: '+id_last_chart);

        for (var u=0; u < selected_objects_chart_list.length; u++){ //Create lists with hosts parameters
          list_charts_pk.push(selected_objects_chart_list[u]['id']);
          list_charts_title.push(selected_objects_chart_list[u]['title']);
          list_charts_xAxis_name.push(selected_objects_chart_list[u]['xAxis_Name']);
          list_charts_yAxis_name.push(selected_objects_chart_list[u]['yAxis_Name']);

          // console.log('Chart div ID:' + list_charts_pk[u])
          //Create Monitoring_Divs
          $("#body_index").prepend("<div class='monitoring_div' ><button type='button' class='btn btn-secondary' id='delete_chart_"+list_charts_pk[u]+"' onclick='Destroy_Chart();'>Delete</button><button type='button' class='btn btn-secondary' id='clear_chart_"+list_charts_pk[u]+"' onclick='Clear_Chart();'>Clean</button> <div class= 'monitoring_chart'  id='chart_"+list_charts_pk[u]+"'  style='width:100%; height:400px;' > </div></div>");

          Monitor_Chart();

        }

      }
      Charts_Reports();

  },
  failure: function(data) {
      alert('Error in Post_Hosts');
  }
});
};

function Get_Chart_Data(){ //Gets GNU Radio monitoring data
  // console.log("Charts Data!");
  $.ajax({
      url: "/gnumonitor/charts_data",
      type: 'GET',
      dataType: 'json',
      data: {id_last_item: id_last_item},
      success: function(data) {

        data_list = data;
        // console.log(data);

        for (i=0; i<objects_chart_list.length;i++){
           var chart_data = data_list.filter(function(p){
             return p.chart_object_id == list_charts_pk[i];});
            Plot_Chart(chart_data, objects_chart_list[i]);
         }
      },
      failure: function(data) {
        alert('Error in Post_Charts');
      }
    });
};

function Plot_Chart(chart_data, object_chart){

  for (var i = 0; i < chart_data.length; i++){
    //Controle do last id pra nao bugar o monitoramento

    // console.log(chart_data[i]);
    if (id_last_item < chart_data[i]['id']){
      id_last_item = chart_data[i]['id'];
    }

    var shift = object_chart.series[0].data.length >= 60;

    var x = new Date(chart_data[i]['time']).getTime();
    var y = chart_data[i]['value'];
    object_chart.series[0].addPoint([x, y], true, shift);
  };
};


function Charts_Reports() {
  $.ajax({
      url: "/gnumonitor/charts_notifications/",
      type: 'GET',
      dataType: 'json',
      data: {id_selected_host: id_selected_host},
      success: function(charts_notes) {
        // REMOVER TODAS DIV
        $("#errors_div").remove();
        console.log('NOTES:'+charts_notes);

        if (charts_notes.length > 0){
          if(!$("#errors_div").length){
            $("#notifications").append("<div id='errors_div'></div>")
          }

          for(var t=0; t< charts_notes.length; t++){
            console.log(charts_notes[t]['etype']);
            if(charts_notes[t]['etype']== 'Warning'){
              $("#errors_div").append("<div class='alert alert-warning' role='alert' id="+charts_notes[t]['id']+" >"+charts_notes[t]['description']+"</div>");
            }

            else if(charts_notes[t]['etype']== 'Error'){
              $("#errors_div").append("<div class='alert alert-danger' role='alert' id="+charts_notes[t]['id']+" >"+charts_notes[t]['description']+"</div>");
            }

            else if(charts_notes[t]['etype']== 'Info'){
              $("#errors_div").append("<div class='alert alert-primary' role='alert' id="+charts_notes[t]['id']+" >"+charts_notes[t]['description']+"</div>");
            }

            else if(charts_notes[t]['etype']== 'Success'){
              $("#errors_div").append("<div class='alert alert-success' role='alert' id="+charts_notes[t]['id']+" >"+charts_notes[t]['description']+"</div>");
            }
            // INSERIR NOVA DIV
          }
        }
        //     $("#errors_div").append("<div class='alert alert-warning' role='alert' id="+charts_notes[i]['id']+" >"+charts_notes[i]['description']+"</div>");
        //   }
        // }
        //
        // else {
        //   if($("#errors_div").length){
        //       $("#errors_div").remove();
        //   }
        // }
      },
      failure: function(errors) {
          alert('Got an error dude');
      }
    });
};


// function Charts_Reports() {
//   $.ajax({
//       url: "/gnumonitor/charts_notifications/",
//       type: 'GET',
//       dataType: 'json',
//       success: function(charts_notes) {
//           // var enable_btn = errorslist.filter(function(p){return p.description == "Warning: No client connection";});
//           // if (enable_btn !== 'undefined' && enable_btn.length == 0){
//           //   $("#add_monitoring").removeClass("nav-link disabled").addClass("nav-link");
//           // }
//           console.log(charts_notes)
//           if (charts_notes.length > 0){
//             if(!$("#errors_div").length){
//               $("#notifications").append("<div id='errors_div'></div>");
//                 // $("#notifications").prepend("<div class='col' id='errors_div'></div>");
//             }
//
//             var new_ids = [];
//             //ADD NEW ERRORS
//             for (i=0; i<charts_notes.length;i++){
//             //for (var error in errorslist ) {
//               //console.log(errorslist[i]['id']);
//               new_ids.push(charts_notes[i]['id']);
//               if(!$('#'+charts_notes[i]['id']).length){
//                 //console.log("Nao Existe");
//                 //$("#errors_reports").append("<p id="+errorslist[i]['id']+" >"+errorslist[i]['chart_object_id']+" "+errorslist[i]['description']+"</p>");
//                 if(charts_notes[i]['etype']=="Error"){
//                   $("#errors_div").append("<div class='alert alert-danger' role='alert' id="+charts_notes[i]['id']+" >"+charts_notes[i]['description']+"</div>");
//                 }
//
//                 else{
//                   $("#errors_div").append("<div class='alert alert-warning' role='alert' id="+charts_notes[i]['id']+" >"+charts_notes[i]['description']+"</div>");
//                 }
//
//               }
//             }
//             //REMOVE SOLVED ERRORS
//             var old_ids = [];
//             var solved_errors = [];
//
//             $("#errors_div").find("div").each(function(){
//               if(this.id>0){
//                 old_ids.push(this.id);
//                 // console.log('ID:' +this.id);
//                 var contem = 0;
//                 for (i=0; i<new_ids.length;i++){//se new_ids nao contem this.id entao faz
//                   //console.log("compara: "+new_ids[i]+ " com"+this.id);
//                   if (parseInt(new_ids[i]) == parseInt(this.id)){
//                     //console.log("deu igual")
//                     contem = 1;
//                     break;
//                   }
//                 }
//                 if(contem == 0){
//                   //console.log("deu DIFERENTE "+ this.id)
//                   $('#'+this.id).remove();
//                   solved_errors.push(this.id)
//                 }
//               }
//             });
//
//
//           } else {
//             if($("#errors_div").length){
//                 $("#errors_div").remove();
//             }
//           }
//
//       },
//       failure: function(errors) {
//           alert('Got an error dude');
//       }
//     });
// };

function Destroy_Chart() {
  var btn = (event.target);
  var raw_chart_pk_to_destroy = btn.id;
  var chart_pk_to_destroy = raw_chart_pk_to_destroy.split("_")[2];
  // console.log(chart_pk_to_destroy);
  $.ajax({
       url:'/gnumonitor/delete_chart/',
       type: 'GET',
       data: {chart_pk_to_destroy: chart_pk_to_destroy},
       success: function() {
           // console.log(chart_pk_to_destroy);
           for (i=0; i<list_charts_pk.length;i++){
             // console.log(list_charts_pk[i]);
             // console.log(chart_pk_to_destroy);
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

function Clear_Chart(cont){
  console.log("clearing chart data!");
  var btn = (event.target);
  var raw_chart_pk_to_clean = btn.id;
  var chart_pk_to_clean = raw_chart_pk_to_clean.split("_")[2];
  // console.log(chart_pk_to_clean);
  // console.log(objects_chart_list);
  for (i=0; i<list_charts_pk.length;i++){
    // console.log(list_charts_pk[i]);
    // console.log(chart_pk_to_clean);

    if (list_charts_pk[i] == chart_pk_to_clean){
      object_chart_to_clear = objects_chart_list[i];
      // console.log("ACHOU"+object_chart_to_clear);
      // for(i=0; i<object_chart_to_clear.series[0].data.length; i++){
      // console.log(object_chart_to_clear.series[0].data.length);
      // object_chart_to_clear.series[0].remove();
      while(object_chart_to_clear.series[0].data.length > 0){
        object_chart_to_clear.series[0].data[0].remove();
      };
      break;
    };
    };
  };

function Grid_Three(){
  $("#body_index").addClass("row");
  $(".monitoring_div").addClass("col");
  // $("#body_index").prepend("<div class='monitoring_div col' style='margin: 5px;' ><button type='button' class='btn btn-secondary' id='delete_chart_{{ chart.pk }}' onclick='Destroy_Chart();'>Delete</button><button type='button' class='btn btn-secondary' id='clear_chart_{{ chart.pk }}' onclick='Clear_Chart();'>Clean</button> <div class= 'monitoring_chart'  id='{{ chart.pk }}'  style='width:100%; height:400px;' > </div></div>");
};

function Grid_List(){
  $("#body_index").removeClass("row");
  $(".monitoring_div").removeClass("col");
  // $("#body_index").prepend("<div class='monitoring_div' style='margin-bottom: 9px;margin-top: 2px;' ><button type='button' class='btn btn-secondary' id='delete_chart_{{ chart.pk }}' onclick='Destroy_Chart();'>Delete</button><button type='button' class='btn btn-secondary' id='clear_chart_{{ chart.pk }}' onclick='Clear_Chart();'>Clean</button> <div class= 'monitoring_chart'  id='{{ chart.pk }}'  style='width:100%; height:400px;' > </div></div>");
};

function Select_Card(){
  var clicked = (event.target);
  // console.log(clicked.id);
  if(clicked.id != ''){
    for(z=0; z<list_hosts_pk.length; z++){
      // console.log("deixa todos os cards brancos");
      $("."+list_hosts_pk[z]+"").removeClass("card_selected");
      $(".monitoring_div").remove();
    }
  // console.log("deixa o card clicado cinza");
  $("."+clicked.id+"").addClass("card_selected");
  id_selected_host= clicked.id;
  id_last_chart=0;
  id_last_item = 0;
  list_charts_pk = [];
  list_charts_title = [];
  list_charts_xAxis_name = [];
  list_charts_yAxis_name = [];
  objects_chart_list = [];
  // console.log("MUDOU O ID NO CLICK!!"+id_selected_host);
  }

};

$(document).ready(function(){
  setInterval(function (){
    Post_Hosts();
    Post_Charts();
    Get_Chart_Data();
    // System_Errors();
    //Charts_Reports();

  }, 1000);
});
