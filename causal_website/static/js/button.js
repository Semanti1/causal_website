
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
    // var socket = io.connect('http://127.0.0.1:5000');

    var object_list = content["object_list"];
    var property_list = content["property_list"];
    var keyword_list = content["keyword_list"];
    var latent_list = content["latent_list"];

    $('#object_words').append("<div class='col-auto text-center' > <p> Object List: </p> </div>");
    $('#object_words').append(load_list(object_list, "obj"));
    $('#property_words').append("<div class='col-auto text-center'> <p> Property List: </p> </div>");
    $('#property_words').append(load_list(property_list, "prop"));
    // $('#property_words2').prepend(load_list(property_list, "prop"));
    // $('#key_words').prepend(load_list(keyword_list, "key"));
    // $('#lat_words').prepend(load_list(latent_list, "lat"));

$(window).on("load", function(){
//   console.log("hello")
  var i = 0;
  $("#property_words2").append("<div class='col-auto text-center'> <p> Property List: </p> </div>");
  $("#key_words").append("<div class='col-auto text-center'> <p> Keyword List: </p> </div>")
  $("#lat_words").append("<div class='col-auto text-center'> <p> Latent List: </p> </div>")

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
  $("#lat_words").append(" <input id='custom_lat' type='text' placeholder='add custom latent' aria-label='add custom latent' >  <button id='lat_add' type='button'>add</button> ");
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
      for (; i <= 5; i++){
        input += "<option value='" + i +"'>" + i + "</option>";
      }
      input += "</select>";
      $("#new_form"+ causal_no).append(input)
    });
  })

  $("#lat_words #lat_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=lat>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })




 });



function load_list(list, id){
	var i = 0;
  var new_input ="";
for(; i < list.length; i++){
   new_input += " <div class='col-auto align-middle' id='" +id +"'> <p>" + list[i] + "</p></div>";
 }
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
    new_input += "<div class ='col-auto'> <input id='object' name='object' class='form-control' list='object_list'>"+ " <datalist id='object_list'>";
  for(; i < object_list.length; i++){
     new_input += " <option value='" + object_list[i] + "'>"
   }
   new_input += "</datalist> </div>"
   new_input += "<div class = ' my-auto'>  's function is to </div>"

  	i = 0;
    new_input += "<div class ='col-auto'> <input id='property' name='property' class='form-control' list='property_list'>"+ " <datalist id='property_list'>";
  for(; i < property_list.length; i++){
     new_input += " <option value='" + property_list[i] + "'>"
   }
   new_input += "</datalist> </div></div>"
   $('#obj_property_form').append(new_input);
   console.log(new_input);
   $('#total_pair').val(new_pair_no)

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
  $("#property_words2").append("<div class='col-auto text-center'> <p> Property List: </p> </div>");
  for (var key in set){
      $("#property_words2").append("<button  id=prop_btn>" + key + "</button>");
  }
  $("#property_words2 #prop_btn").each(function(index){
    $(this).on('click', function(){
      var causal_no = parseInt($('#total_object_causal').val());
      $("<div class='col-auto align-middle' id=prop>" + $(this).text()+ "</div>").appendTo("#new_form"+ causal_no);
    });
  })

  // $("#text_obj").text(content);
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

function add_causal(){
  var new_causal_no = parseInt($('#total_object_causal').val())
  if (new_causal_no ==0){
    new_causal_no =+1;
    $('#total_object_causal').val(new_causal_no)
    var new_input = " <div class='row' id='new_form" + new_causal_no +  "'>";
    new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
    new_input += "<div class=' my-auto'> Causal rule #" + new_causal_no + ": </div>"
    $("#object_causal").append(new_input);

  }else{
    var prev_causal = $("#new_form" + (new_causal_no))
    var prev_causal_obj = prev_causal.find(".col-auto");
    sentence = []
    $.each(prev_causal_obj, function(){
      var obj_name = $(this).text();
      var obj_type = $(this).attr("id");
      sentence.push(obj_type + ":" + obj_name);
    })
    console.log(sentence)
    $.ajax({
      type:"POST",
      url:"/check_correct",
      data: JSON.stringify(sentence),
      contentType:"application/json; charset=utf-8",
      success: function(data){
        console.log(data)
        if (data){
              new_causal_no +=1;
              $('#total_object_causal').val(new_causal_no);
              var new_input = "</div> <div class='row' id='new_form" + new_causal_no +  "'>";
              new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
              new_input += "<div class=' my-auto'> Causal rule #" + new_causal_no + ": </div>"
              // new_input += "<button type=button class=close aria-label=Close> <span aria-hidden='true'>&times;</span></button>"
              $("#object_causal").append(new_input);
        }
        else{
          $("#text_causal").empty()
          $("#text_causal").text("syntax error");
        }
      }
    });
  }

}

$(document).on('click', "#object_causal .row .close", function(){
  $(this).parent().remove();
})



function extract_causal(){
  var row = $("#object_causal").find(".row");
  all_sentences = []
  $.each(row, function(){
    sentence = []
    var object = $(this).find('.col-auto');
      $.each(object, function(){
      var obj_name = $(this).text();
      var obj_type = $(this).attr("id");
      sentence.push(obj_type + ":" + obj_name);
    })
    var object = $(this).find("select")
    if (object.length > 0){
      var obj_value = object.find(":selected").text();
      sentence.push("extend:"+obj_value);
    }
    all_sentences.push(sentence);
  });
  return all_sentences;
}

function generate_causal(){
  var all_sentences = extract_causal();
  console.log(all_sentences);
   $.ajax({
     type:"POST",
     url: "/recieve_causal",
     data: JSON.stringify(all_sentences),
     contentType:"application/json; charset=utf-8",
     success:function(msg){
       $("#image_causal").empty();
       console.log(msg)
       var content = "<img src='/" + msg + ".png' class='img-fluid' alt='Responsive Image'>"
       $("#image_causal").append(content);
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



function submit_causal(){
   // console.log($("#object_causal")[0])
   var row = $("#object_causal").find(".row");
   var all_sentences = extract_causal();

   $.ajax({
     type:"POST",
     url: "/submit_causal",
     data: JSON.stringify(all_sentences),
     contentType:"application/json; charset=utf-8",
     success: function(msg){
       $("#text_causal").empty();
       $("#image_causal").append("<p style='color:blue;' >" + msg + "</p>");
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
