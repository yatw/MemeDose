$(document).ready(function() {
	
	$("#loading_alert").hide();
	$("#jojo_alert").hide();
	$("#error_alert").hide();
	$("#nothing_alert").hide();
	
	$('button').click(function(event) {
	   $("#error_alert").hide();
	   $("#nothing_alert").hide();

	   var meme_sub = event.target.id;
	   var sortby = document.getElementById('sortby').value
	   var quantity = document.getElementById('quantity').value
	   
	   if (meme_sub == "ShitPostCrusaders"){
		   $("#jojo_alert").html('Good Job!').removeClass("hide").hide().fadeIn("slow");
	   }else{
		   $("#loading_alert").html('Fetching the meme...').removeClass("hide").hide().fadeIn("slow");
	   }

		$.ajax({
			url: "/display_meme",
			type: "get",
			data: {meme_sub: meme_sub, sortby: sortby, quantity: quantity},
			success: function(response) {
				
				display_meme(response.memelist)
			    $("#jojo_alert").hide();
				$("#loading_alert").hide();
				
				if (response.memelist.length == 0){
					$("#nothing_alert").show();
				}

		},
			error: function(xhr) {
				$("#error_alert").show();
		}})
	});   
});

function display_meme(memelist){
	
	var content = ""
	
	//<img src="cinqueterre.jpg" class="img-rounded" alt="Cinque Terre"> 

	for (i = 0; i < memelist.length; i++){
		content += "<img src=" + memelist[i] + " style=\"width:640px;height:480px;border:0;\""  +  ">"
		content += "<hr>"
	}
	document.getElementById('meme_display').innerHTML = content;
	
}

