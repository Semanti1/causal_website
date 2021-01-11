
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
    var socket = io.connect('http://127.0.0.1:5000');

    var object_list = content["object_list"];
    var property_list = content["property_list"];
    var keyword_list = content["keyword_list"];
    var latent_list = content["latent_list"];

    $('#object_words').append("<div class='col-xs-2 text-center' > <p> Object List: </p> </div>");
    $('#object_words').append(load_list(object_list, "obj"));
    $('#property_words').append("<div class='col-xs-2 text-center'> <p> Property List: </p> </div>");
    $('#property_words').append(load_list(property_list, "prop"));
    $('#property_words2').prepend(load_list(property_list, "prop"));
    $('#key_words').prepend(load_list(keyword_list, "key"));
    $('#lat_words').prepend(load_list(latent_list, "lat"));

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
   new_input += "<div class = 'col-auto'> <p class='text-center'>has</p> </div>"

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

function serialize(){
  var form = $("#obj_property_form");
  //var content = getFormData(form);
  var content = JSON.stringify(form.serializeArray())
  //$.post("/recieve_property", content)
  $.ajax({
    type:"POST",
    url: "/recieve_property",
    data: content,
    contentType:"application/json; charset=utf-8",
  });
  console.log(content);
  $("#text_obj").text(content);
}

function add_causal(){
  var new_causal_no = parseInt($('#total_object_causal').val())+1;
  $('#total_object_causal').val(new_causal_no)
  if (new_causal_no ==2){
    var new_input = " <form> <div class='form-group row' id='new_form" + new_causal_no +  "'>";

  }else{
    var new_input = "</div> </form> <form><div class='form-group row' id='new_form" + new_causal_no +  "'>";

  }
  new_input += "<p> Causal rule #" + new_causal_no + ": </p>"
  $("#object_causal").append(new_input);

}

function generate_causal(){
 // console.log($("#object_causal")[0])
 var object = $("#object_causal").find("form");
 var all_sentences = []
 $("#text_causal").empty();
 $.each(object, function(){
   var x = $(this).serializeArray();
   var sentence = []
   $.each(x, function(i, field){
     $("#text_causal").append(field.name + ": " + field.value + " ");
     sentence.push(field.name + ":" + field.value);
   })
   all_sentences.push(sentence);
   $("#text_causal").append("</p>");
 })
 $.ajax({
   type:"POST",
   url: "/recieve_causal",
   data: JSON.stringify(all_sentences),
   contentType:"application/json; charset=utf-8",
 });


 console.log(all_sentences)
}

socket.on("causal graph", function(msg){
    // $("#image_causal").append("<p>" + msg+ "</p>");
    $("#image_causal").empty();
    var content = "<img src='/" + msg + ".png' class='img-fluid' alt='Responsive Image'>"
    $("#image_causal").append(content);
    // $("#image_causal").attr("src", "/"+msg+".png");
  });


function submit_causal(){
   // console.log($("#object_causal")[0])
   var object = $("#object_causal").find("form");
   var all_sentences = []
   $.each(object, function(){
     var x = $(this).serializeArray();
     var sentence = []
     $.each(x, function(i, field){
       sentence.push(field.name + ":" + field.value);
     })
     all_sentences.push(sentence);
   })
   $.ajax({
     type:"POST",
     url: "/submit_causal",
     data: JSON.stringify(all_sentences),
     contentType:"application/json; charset=utf-8",
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
