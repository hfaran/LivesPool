// TODO: implement proper action for errors in API calls
// TODO: functionality for balls per player value
// TODO: disable form for number of balls if user isn't owner of room

function load_players(container) {
	$.ajax({
		url: "/api/room/listplayers",
		success: function(data) {
			$(container).empty();
			$(container).append('<ul id="playerlist" class="list-group"></ul>');

			var firstItem = true;
            $.each(data["data"]["players"], function(key, value) {
            	
            	if(firstItem) {
        			$("ul#playerlist").append('<li class="list-group-item owner">' + value + '</li>');
            		firstItem = false;
            	}
            	else {
            		$("ul#playerlist").append('<li class="list-group-item">' + value + '</li>');
            	}

            });
		}
	});
}

function leave_room() {
	$('#leaveroombutton').click(function() {
		$.ajax({
			url: "/api/room/leaveroom",
			type: "DELETE",
			success: function() {
				window.location.href = "/room/join";
			},
			error: function() {
				alert("Owners cannot leave room. You must retire the room.");
				// TODO: wait for refactoring involved in Issue #63 
			}
		});
	});
}

function create_game() {
	$('#numBallsForm').submit(function(event) {
		event.preventDefault();
		
		var num = parseInt($("#inputNumBalls").val());
		
		$.ajax({
			type: "POST",
			url: "/api/game/creategame",
			data: JSON.stringify({nbpp: num}),
			content_type: "application/json; charset=utf-8",
			dataType: "json",
			success: function() {
				window.location.href = "/room/game"
			},
			error: function(jqXHR, status, error) {
				// TODO: implement
			}
		});
	});
}

$(document).ready(function() {
	load_players("#lobby_container");
	create_game();
	leave_room();
});
