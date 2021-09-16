
  	$('#add_property').on('click', add_property_handler);
    $('#remove_property').on('click', remove_property);
		$('#add_object').on('click', add_object_handler);
    $('#remove_object').on('click', remove_object);
    $('#add_object_properties').on('click', add_object_properties_handler);
    $('#submit').on('click', serialize);
    $('#add_keywords').on('click', add_keywords_handler);
    $('#remove_keywords').on('click', remove_keywords);
    $('#add_latent').on('click', add_latent_handler);
    $('#remove_latent').on('click', remove_latent);
    $('#add_causal').on('click', add_causal);
    $('#generate_causal').on('click', generate_causal);
    $('#submit_causal').on('click', submit_causal);
    $('#add_graph').on('click', add_graph)
    $('#planner').on('click', plan_causal);
    $('#add_plan_object_properties').on('click', add_plan_object_properties);
    $('#plan_submit').on('click', plan_submit);
    $("#next_step").on('click', next_step);
    // var socket = io.connect('http://127.0.0.1:5000');

    //var object_list = content["object_list"];
    var object_dict = allobject;
    var object_list=[]
    var property_list = content["property_list"];
    var total_property_list = [];
    //var keyword_list = content["keyword_list"];
    var keyword_list = ["AND", "OR", "is/are neccesary for causing"];
    var latent_list = content["latent_list"];
    //var goal_list = content["goal_list"];
    var goal_list = ["Light"]
    var plan_object_list = []
    var plan_object_dict = {}
    var plan_property_list = []
    if(typeof all_planobject !== 'undefined'){
      plan_property_list = plan_content["property_list"];
      plan_object_dict = all_planobject

    }
    for(var key in object_dict){
      // $('#object_words').append();
      $('#object_words').append(load_list(object_dict[key], "obj", key));
      for (var key2 in object_dict[key]){
        object_list.push(object_dict[key][key2]);
      }
    }
    // if (property_list.length !=0){
    //   $('#property_words').append("<div class='col-auto text-center'> <p> Function(s) of object parts: </p> </div>");
    //   $('#property_words').append(load_list(property_list, "prop"));
    // }

    // $('#plan_object_words').append("<div class='col-auto text-center' > <p> Object parts: </p> </div>");
    for(var key in plan_object_dict){
      console.log(key, plan_object_dict[key])
      $('#plan_object_words').append(load_list(plan_object_dict[key], "obj", key));
      for(var key2 in plan_object_dict[key]){
        plan_object_list.push(plan_object_dict[key][key2]);
      }
    }

    console.log(alldescription)
    if(alldescription.length < 4){
      for(var i = 0; i < alldescription.length; i++){
      $("#furntiure_description").append("<div class='col'> <p>" + alldescription[i]+"</p></div>");
      }
    }
    if(typeof allplandescription !=="undefined"){
      if(allplandescription.length == 1){
        $("#plan_furniture_img").append("<div class='col' <p>" + allplandescription[0] + "</p></div>")
      }
    }

    // $('#property_words2').prepend(load_list(property_list, "prop"));
    // $('#key_words').prepend(load_list(keyword_list, "key"));
    // $('#lat_words').prepend(load_list(latent_list, "lat"));

$(window).on("load", function(){
//   console.log("hello")
  var href = window.location.href;
  var rel_href = href.replace(/^(?:\/\/|[^/]+)*\//, '')
  console.log(rel_href)
  // if(rel_href == "light"){
  //   console.log("here")
  //   $("#txt_for_all").append("<p> In this task, your goal is to create a single causal model that can explain how all four objects create light. That is, you need to consider which object parts from different objects plays the same role in creating light, and use these functions in creating a generalized causal model for producing light</p>")
  // }else {
  document.getElementById("MORESTEP").style.display='none'

  // }
  var i = 0;
  $("#property_words2").append("<div class='col-auto text-center'> <p> Function(s) of object parts List: </p> </div>");
  $("#key_words").append("<div class='col-auto text-center'> <p> Keywords: </p> </div>")
  $("#lat_words").append("<div class='col-auto text-center'> <p> Effect: </p> </div>")
  $("#goal_words").append("<div class='col-auto text-center'> <p> Goal: </p> </div>")
  // for (; i < property_list.length; i++){
  //   $("#property_words2").append("<button  id=prop_btn>" + property_list[i] + "</button>");
  // }
  for (i = 0; i < keyword_list.length; i++){
    if (keyword_list[i].indexOf("preferrable") !=-1){
      $("#key_words").append("<button id=key_btn_special>" + keyword_list[i] + "</button> ");
    }else{
      $("#key_words").append("<button id=key_btn>" + keyword_list[i] + "</button>");
    }
  }

  for (i = 0; i < latent_list.length; i++){
    $("#lat_words").append("<button  id=lat_btn>" + latent_list[i] + "</button>");
  }

  for (i = 0; i < goal_list.length; i++){
    $("#goal_words").append("<button  id=goal_btn>" + goal_list[i] + "</button>");
  }

  $("#lat_words").append(" <input id='custom_lat' type='text' placeholder='add an effect' aria-label='add custom latent' >  <button id='lat_add' type='button'>add</button> ");
  $("#lat_add").on('click', function(){
    var text = $("#custom_lat").val();
    var lat_no = parseInt($("#total_latent").val());
    $("<button id='lat_add_btn" + lat_no + "'>" + text + "</button>").insertBefore('#custom_lat');
    $("#lat_add_btn" + lat_no).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=lat>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    })
    $("#total_latent").val(lat_no+1);

  })



  $("#key_words #key_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=key>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })

  $("#key_words #key_btn_special").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=key>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
      var input = "<select id='score'>";
      var i =1;
      for (; i <= 7; i++){
        input += "<option value='" + i +"'>" + i + "</option>";
      }
      input += "</select>";

      $("#new_form"+causal_no +" #prop").after(input)
      $("#new_form"+causal_no + " #lat").after(input)

    });
  })

  $("#lat_words #lat_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=lat>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })
  $("#goal_words #goal_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=goal>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })

  $('#plan_property_words').append("<div class='col-auto text-center'> <p> Function(s) of object parts: </p> </div>");
  if (plan_property_list.length !=0){
    $('#plan_property_words').append(load_list(plan_property_list, "prop"));
  }


 });

 // $("#add_causal").each(function(index){
 //   $(this).on('click', function(){
 //     var causal_graph_no = parseInt($('#total_causal_graph').val());
 //     var input = "<select id='graph'>";
 //     for (var i = 0; i < causal_graph_no+1; i++){
 //       input += "<option value='" + i +"'>" + "causal_graph" + i + "</option>";
 //     }
 //     input += "</select>";
 //
 //     $("#add_causal").append(input);
 //
 //   });
 // })



function load_list(list, id, name){
	var i = 0;
  var new_input ="<div class='row'> <div class='col-auto text-center' > <p> Object parts for " + name +  ":  </p> </div>";
for(; i < list.length; i++){
   new_input += " <div class='col-auto align-middle' id='" +id +"'> <p>" + list[i] + "</p></div>";
 }
 new_input+= "</div> "
 return new_input;
}
function add_object_handler(){
  add_object(object_list);
}

function add_object(object_list){
	var i = 0;
  var new_obj_no = parseInt($('#total_obj').val()) + 1;
  var new_causal_no = parseInt($('#total_object_causal').val());
  var new_input = "<div class ='col-xs-2' id='new_obj" + new_obj_no+"'>" + "<input class='form-control' id =object list='object_list' >"+ " <datalist id='object_list'>";
for(; i < object_list.length; i++){
   new_input += " <option value='" + object_list[i] + "'>"
 }
 new_input += "</datalist> </div>"

  $('#new_form'+ new_causal_no).append(new_input);

  $('#total_obj').val(new_obj_no);
}

function add_property_handler(){
  add_property(property_list);
}

function add_property(property_list) {
	var i = 0;
  var new_prop_no = parseInt($('#total_prop').val()) + 1;
  var new_causal_no = parseInt($('#total_object_causal').val());
  var new_input = "<div class ='col-auto' id='new_prop" + new_prop_no+"'>" + "<input class='form-control' name=property id=property list='property_list' >"+ " <datalist id='property_list'>";
/*   + "<option value = 'connection to power source'>"+
  "<option value = 'production' >" + "</datalist>" */;
for(; i < property_list.length; i++){
   new_input += " <option value='" + property_list[i] + "'>"
 }
 new_input += "</datalist></div>"

  $('#new_form'+new_causal_no).append(new_input);

  $('#total_prop').val(new_prop_no);
}



function add_keywords_handler(){
  add_keywords(keyword_list);
}
function add_keywords(keyword_list) {
  	var i = 0;
    var new_kw_no = parseInt($('#total_kw').val()) + 1;
    var new_causal_no = parseInt($('#total_object_causal').val());
    var new_input = "<div class ='col-auto' id='new_key" + new_kw_no+"'>" +
    "<input class='form-control' name=keyword id=keyword list='keyword_list'  >"+
     " <datalist id='keyword_list'>";
  /*   + "<option value = 'connection to power source'>"+
    "<option value = 'production' >" + "</datalist>" */;
  for(; i < keyword_list.length; i++){
     new_input += " <option value='" + keyword_list[i] + "'>"
   }
   new_input += "</datalist></div>"

    $('#new_form'+new_causal_no).append(new_input);

    $('#total_kw').val(new_kw_no);
}

function add_latent_handler(){
  add_latent(latent_list);
}

function add_latent(latent_list) {
  var i = 0;
  var new_lat_no = parseInt($('#total_latent').val()) + 1;
  var new_causal_no = parseInt($('#total_object_causal').val());
  var new_input = "<div class ='col-auto' id='new_latent" + new_lat_no+"'>" + "<input class='form-control' name=latent id=latent list='latent_list' >"+ " <datalist id='latent_list'>";
/*   + "<option value = 'connection to power source'>"+
  "<option value = 'production' >" + "</datalist>" */;
for(; i < latent_list.length; i++){
   new_input += " <option value='" + latent_list[i] + "'>"
 }
 new_input += "</datalist></div>"

  $('#new_form'+new_causal_no).append(new_input);

  $('#total_latent').val(new_lat_no);
}

function add_object_properties_handler(){
  add_object_properties(object_list, property_list);
}

function add_object_properties(object_list, property_list) {
  	var i = 0;
    var new_pair_no = parseInt($('#total_pair').val()) + 1;
    var new_input = " <div class='form-group row' id='new_pair_" + new_pair_no+"'>";
  new_input += "<div class ='col-auto'> <input id='object' onkeydown='return false;' name='object' class='form-control' list='object_list'>"+ " <datalist id='object_list'>";
  // new_input += "<div class= 'col-auto'> <select id='object'> "
  for(; i < object_list.length; i++){
     new_input += " <option value='" + object_list[i] + "'>" + object_list[i] + "</option>"
   }
   new_input += "</datalist> </div>"
   new_input += "<div class = ' my-auto'>  's function is to </div>"

  	i = 0;
    new_input += "<div class ='col-auto'> <input id='property' name='property' class='form-control' list='property_list'>"+ " <datalist id='property_list'>";
  for(; i < property_list.length; i++){
     new_input += " <option value='" + property_list[i] + "'>"
   }
   new_input += "</datalist> </div></div>"
   $('#obj_property_form').prepend(new_input);
   console.log(new_input);
   $('#total_pair').val(new_pair_no)

   $('#object').on('click', function() {
    $(this).val('');
  });

}

function add_plan_object_properties(){
  var i = 0;
  var new_pair_no = parseInt($('#total_pair').val()) + 1;
  var new_input = " <div class='form-group row' id='new_pair_" + new_pair_no+"'>";
  new_input += "<div class ='col-auto'> <input id='object' onkeydown='return false;' name='object' class='form-control' list='plan_object_list'>"+ " <datalist id='plan_object_list'>";
  console.log(plan_object_list)
  for(; i < plan_object_list.length; i++){
    new_input += " <option value='" + plan_object_list[i] + "'>" + plan_object_list[i] + "</option>"
  }
 new_input += "</datalist> </div>"
 new_input += "<div class = ' my-auto'>  's function is to </div>"

  i = 0;
  new_input += "<div class ='col-auto'> <input id='property' onkeydown='return false;' name='property' class='form-control' list='total_property_list'>"+ " <datalist id='total_property_list'>";
  for(; i < total_property_list.length; i++){
   new_input += " <option value='" + total_property_list[i] + "'>" + total_property_list[i] + "</option>"
 }
 new_input += " <option value='None of above'> None of above </option>"
 new_input += "</datalist> </div></div>"
 $('#plan_obj_property_form').prepend(new_input);
 $('#total_pair').val(new_pair_no)

  $('#plan_obj_property_form #object').on('click', function() {
    $(this).val('');
  });

  $('#plan_obj_property_form #property').on('click', function() {
    $(this).val('');
  });
}

function getFormData($form){
  var unindexed_array = $form.serializeArray();
  var indexed_array = {};

  $.map(unindexed_array, function(n,i){
    indexed_array[n['name']] = n['value'];
  });
  return indexed_array;
}

function onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}

function serialize(){
  var form = $("#obj_property_form");
  var content = JSON.stringify(form.serializeArray());
  console.log(content)
  //$.post("/recieve_property", content)
  $.ajax({
    type:"POST",
    url: "/recieve_property",
    data: content,
    contentType:"application/json; charset=utf-8",
  });

  var property_list = form.serializeArray().map(function(v){
    if (v.name =="property"){
      return [v.value];
    }
  })
  var set = {};
  $.each(property_list, function(index, value){
    if (value != undefined){
      set[value] = 1;
    }
  })

  var i = 0;
  $("#property_words2").empty()
  $("#property_words2").append("<div class='col-auto text-center'> <p> Function(s) of object parts: </p> </div>");
  for (var key in set){
      $("#property_words2").append("<button  id=prop_btn>" + key + "</button>");
      total_property_list.push(key)
  }
  $("#property_words2 #prop_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=prop>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })

  $("#plan_property_words").empty()
  $("#plan_property_words").append("<div class='col-auto text-center'> <p> Function(s) of object parts: </p> </div>");
  for (var key in set){
      $("#plan_property_words").append( "<div class='col-auto align-middle' id='prop'><p>" + key + "</p></div>");
  }

  // $("#text_obj").text(content);
}

function plan_submit(){
  var form = $("#plan_obj_property_form");
  var content = JSON.stringify(form.serializeArray());
  //$.post("/recieve_property", content)
  $.ajax({
    type:"POST",
    url: "/recieve_plan_property",
    data: content,
    contentType:"application/json; charset=utf-8",
    success: function(msg){
      console.log(msg)
      if(msg=="OK"){
        $("#text_step3").text("successfully saved.")
      }
    }
  });
}

// function add_causal(){
//   var new_causal_no = parseInt($('#total_object_causal').val())+1;
//   $('#total_object_causal').val(new_causal_no)
//   if (new_causal_no ==2){
//     var new_input = " <form> <div class='form-group row' id='new_form" + new_causal_no +  "'>";
//
//   }else{
//     var new_input = "</div> </form> <form><div class='form-group row' id='new_form" + new_causal_no +  "'>";
//
//   }
//   new_input += "<p> Causal rule #" + new_causal_no + ": </p>"
//   $("#object_causal").append(new_input);
//
// }
function add_graph(){
  var causal_graph_no = parseInt($('#total_causal_graph').val())
  var rel_causal_no = parseInt($('#relevant_object_causal').val())
  causal_graph_no  = causal_graph_no + 1;
  rel_causal_no = 0;
  $('#relevant_object_causal').val(rel_causal_no); //reset relevant object causal rule no when create a new causal graph
  $("#total_causal_graph").val(causal_graph_no);
  new_input = "<div id='object_causal" + causal_graph_no + "'> <p> <strong>causal_graph " + (causal_graph_no+1) + "</strong></p>"
  $("#causal_graph").append(new_input)
  var input = "<option value='" + causal_graph_no +"'> to causal_graph " + (causal_graph_no+1) + "</option>";
  $("#graph").append(input)
  $("#graph").val(causal_graph_no).change();
  $("graph").text("to causal_graph "+ (causal_graph_no+1)).change()
  add_causal();
}


function add_causal(){
  var new_causal_no = parseInt($('#total_object_causal').val())
  var rel_causal_no = parseInt($('#relevant_object_causal').val())
  var reset_causal_delete = parseInt($('#reset_causal_delete').val())
  //var causal_graph_no = parseInt($('#total_causal_graph').val())
  var causal_graph_no = $("#graph").val()
  console.log(causal_graph_no)
  if (rel_causal_no ==0 ){
    new_causal_no +=1;
    rel_causal_no +=1;
    $('#total_object_causal').val(new_causal_no)
    $("#relevant_object_causal").val(rel_causal_no);
    var new_input = " <div class='row' id='new_form" + new_causal_no +  "'>";
    new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
    new_input += "<div class=' my-auto'> Causal rule #" + new_causal_no + ": </div>"
    $("#object_causal"+ causal_graph_no).append(new_input);
  }
  else if(reset_causal_delete){
    new_causal_no +=1;
    rel_causal_no +=1;
    $('#total_object_causal').val(new_causal_no)
    $("#relevant_object_causal").val(rel_causal_no);
    var new_input = " <div class='row' id='new_form" + new_causal_no +  "'>";
    new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
    new_input += "<div class=' my-auto'> Causal rule #" + new_causal_no + ": </div>"
    $("#object_causal"+ causal_graph_no).append(new_input);
    $("#reset_causal_delete").val(0);
  }
    else{
    var prev_causal = $("#new_form" + (new_causal_no))
    var prev_causal_obj = prev_causal.find(".col-auto, select");
    sentence = []
    $.each(prev_causal_obj, function(){
      var obj_type = $(this).attr("id");
      var obj_name = $(this).text();

      if(obj_type == "score"){
        obj_name = $(this).find(":selected").text();
        //obj_name = $(this).attr("selected", "selected")
      }
      sentence.push(obj_type + ":" + obj_name);
    })
    console.log(sentence)

    $.ajax({
      type:"POST",
      url:"/check_correct",
      data: JSON.stringify(sentence),
      contentType:"application/json; charset=utf-8",
      success: function(msg){
        console.log(msg)
        if (msg=="success"){
          $("#text_causal").empty()
          new_causal_no +=1;
          rel_causal_no +=1
          $('#total_object_causal').val(new_causal_no);
          $("#relevant_object_causal").val(rel_causal_no);
          var new_input = "</div> <div class='row' id='new_form" + new_causal_no +  "'>";
          new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
          new_input += "<div class=' my-auto'> Causal rule #" + new_causal_no + ": </div>"
          // new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
          $("#object_causal"+causal_graph_no).append(new_input);
        }
        else{
          $("#text_causal").empty()
          $("#text_causal").text(msg);
        }
      }
    });
  }

}

$(document).on('click',  ".row .close", function(){
  $(this).parent().remove();
  $("#text_causal").empty()
  //var causal_no = parseInt($('#total_object_causal').val())
  //causal_no = causal_no -1;
  //console.log(causal_no)
  //$('#total_object_causal').val(causal_no)
  $('#reset_causal_delete').val(1);
})



function extract_causal(i){
  var row = $("#object_causal"+i).find(".row");
  all_sentences = []
  $.each(row, function(){
    sentence = []
    var object = $(this).find('.col-auto, select');
      $.each(object, function(){
        var obj_type = $(this).attr("id");
        var obj_name = $(this).text();

        if(obj_type == "score"){
          obj_name = $(this).find(":selected").text();
          //console.log($(this).filter(":selected"))
          //console.log($(this).find(":selected").text());

          //obj_name = $(this).filter('option:selected').text();
        }
        sentence.push(obj_type + ":" + obj_name);
    });


    all_sentences.push(sentence);
  });
  return all_sentences;
}

function generate_causal(){
  var i = 0;
  var all_sentences = []
  var total_causal_graph_no = parseInt($("#total_causal_graph").val());
  for(; i < (total_causal_graph_no+1); i++){
    //var row = $("#object_causal" + i).find(".row");
    var sentences = extract_causal(i);
    console.log(sentences);
    all_sentences.push(sentences);
  }
  console.log(all_sentences);
   $.ajax({
     type:"POST",
     url: "/recieve_causal",
     data: JSON.stringify(all_sentences),
     contentType:"application/json; charset=utf-8",
     success:function(msg){
       $("#image_causal").empty();
       console.log(msg)
      for (var i = 0; i < msg.length; i++){
        var content = "<img src='/" + msg[i] + ".png' class='img-fluid' alt='Responsive Image'>"
        $("#image_causal").append(content);
      }
     }
   });
}

function plan_causal(){
  var href = window.location.href;
  var rel_href = href.replace(/^(?:\/\/|[^/]+)*\//, '')
  console.log(rel_href)
  $.ajax({
    type:"POST",
    url: "/plan_causal",
    data:{"obj": rel_href},
    //contentType:"application/json; charset=utf-8",
    success: function(msg){
      console.log(msg)
      $("#plan").empty();
      $("#plan").append("<p>")
      if(msg.length == 0){
        $("#plan").append("Failed to generate a plan");
      }else{
        for(var i = 0; i < msg.length; i++){
          $("#plan").append("Plan " + i + " : " + msg[i] + "<br>");
        }
      }
      $("#plan").append("</p>")
    }
  });
}
//
//  console.log(all_sentences)
// }

//
// socket.on("save success", function(msg){
//     // $("#image_causal").append("<p>" + msg+ "</p>");
//     $("#text_causal").empty();
//     $("#image_causal").append("<p style='color:blue;' >" + msg + "</p>");
//     // $("#image_causal").attr("src", "/"+msg+".png");
//   });
//
// socket.on("save failure", function(msg){
//     // $("#image_causal").append("<p>" + msg+ "</p>");
//     $("#text_causal").empty();
//     $("#image_causal").append("<p style='color:red;'>" + msg + "</p>");
//     // $("#image_causal").attr("src", "/"+msg+".png");
//   });

function next_step(){
    var x = document.getElementById("MORESTEP");
   if(x.style.display == "none"){
     x.style.display = "block";
   }
   document.getElementById("submit_causal").disabled = true;

}

function submit_causal(){
   // console.log($("#object_causal")[0])
   var i = 0;
   var all_sentences = []
   var total_causal_graph_no = parseInt($("#total_causal_graph").val());
   console.log(total_causal_graph_no)
   for(; i < (total_causal_graph_no+1); i++){
     //var row = $("#object_causal" + i).find(".row");
     var sentences = extract_causal(i);
     console.log(sentences);
     all_sentences.push(sentences);
   }
   var submit_time = parseInt($("#total_submit_times").val())
   submit_time +=1;
   $("#total_submit_times").val(submit_time);

   //checking for resubmit
   $.ajax({
     type:"POST",
     url: "/submit_causal",
     data: JSON.stringify(all_sentences),
     contentType:"application/json; charset=utf-8",
     success: function(msg){
       $("#text_causal").empty();
       $("#text_causal").append("<p style='color:blue;' >" + msg + "</p>");
     }
   });
   $.ajax({
     type:"POST",
     url: "/record_time",
     data: JSON.stringify({"time": submit_time}),
     contentType:"application/json; charset=utf-8",
     success: function(msg){
     }
   });



   console.log(all_sentences)
  }



function remove_property() {
  var last_prop_no = $('#total_prop').val();

  if (last_prop_no > 1) {
    $('#new_prop' + last_prop_no).remove();
    $('#total_prop').val(last_prop_no - 1);
  }
}

function remove_object(){
  var last_obj_no = $('#total_obj').val();
  if (last_obj_no > 1) {
    $('#new_obj' + last_obj_no).remove();
    $('#total_obj').val(last_obj_no - 1);
  }
}

function remove_keywords(){
  var last_obj_no = $('#total_kw').val();
  if (last_obj_no > 1) {
    $('#new_key' + last_obj_no).remove();
    $('#total_kw').val(last_obj_no - 1);
  }
}

function remove_latent(){
  var last_obj_no = $('#total_latent').val();
  if (last_obj_no > 1) {
    $('#new_latent' + last_obj_no).remove();
    $('#total_latent').val(last_obj_no - 1);
  }
}
