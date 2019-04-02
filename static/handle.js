

$('#musiccontrol').click(function(){
	
	var player = document.getElementById('music_player');
	
	if (player.paused){
		$("#musiccontrol").html("Pause Music");
		player.play();
	}else{
		$("#musiccontrol").html("Play Music");
		player.pause();		
	}
});

$('#restartbtn').click(function(){
	$("#gameresult").hide();
	
	$.getJSON($SCRIPT_ROOT + '/_restart_game', {}, function(data) {
	});
	
	clean_table();
});

function clean_table(){
	
	var t = document.getElementById('gamegrid');
	
	for (var r = 0; r <= 5; r++){		
		for (var c = 0; c <=6 ; c++){
			t.rows[r+1].cells[c].innerHTML = '0';
			t.rows[r+1].cells[c].setAttribute("style", "background:#FFFFFF;");
		}
	}
}


$(document).ready(function() {

	var game_on = true;
	$("#gameresult").hide();
	
	
	$.ajaxSetup({
		async: false
	})
	
	$('td').click(function(){
		
		$.getJSON($SCRIPT_ROOT + '/_game_status', {}, function(data) {
			if (data.game_status == "True"){
				game_on = true;
			}
		});
		
		if (game_on){
			
			var col = $(this).parent().children().index($(this));
			var row = $(this).parent().parent().children().index($(this).parent());
			//console.log('Column: ' + col);
			
			$.getJSON($SCRIPT_ROOT + '/_player_move', {
				column: col
			}, function(data) {
				
				if (data.row >= 0){		
					var t = document.getElementById('gamegrid');
					t.rows[data.row+1].cells[col].innerHTML = data.color;

					if (data.color == "1"){
						t.rows[data.row+1].cells[col].setAttribute("style", "background:#F47983;");
						$("#whowin").html("<strong>Red Win!!</strong>");
					}else{
						t.rows[data.row+1].cells[col].setAttribute("style", "background:#f4ce42;");
						$("#whowin").html("<strong>Yellow Win!!</strong>");
					}
				
					if (data.win == "True"){
						game_on = false;
						$("#gameresult").show();
					}else if (data.tie == "True"){
						$("#whowin").html("<strong>This is a Tie!!</strong>");
						game_on = false;
						$("#gameresult").show();
					}	
				}
			});
		}else{
			console.log("Already Game Over")
		}

	});
});
