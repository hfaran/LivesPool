function load_rooms() {
    $.ajax({
        url: "/api/room/listrooms",
        success: function(data) {
            $("#room_container").empty();
            if (data["data"].length == 0) {
                $("#room_container").append('<button class="btn btn-default btn-primary btn-block">Create a Room</button>').click(function() {window.location.href ="/room/create";});
            } else {
                $.each(data["data"], function(index, value) {
                    $("#room_container").append('<button class="btn btn-default btn-primary btn-block">' + value["name"] + '</button>');
                });
            }
        }
    });

    setTimeout(load_rooms, 5000);
}

$(document).ready(function() {
    load_rooms();
});
