function load_players() {
	$.ajax({
		url: "/api/room/listplayers",
		success: function(data) {
			$("#lobby_container").empty();
			$("#lobby_container").append('<ul id="playerlist" class="list-group"></ul>');
			
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

$(document).ready(function() {
	load_players();
	// TODO: functionality for Start Game
	// TODO: functionality for Leave Game
	// TODO: functionality for balls per player value
	// TODO: disable form for number of balls if user isn't owner of room
});