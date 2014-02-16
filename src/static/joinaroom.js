function join_room(name) {
    $.ajax({
        type: "POST",
        url: "/api/room/joinroom",
        data: '{"name":"' + name + '"}',
        success: function () {
            window.location.href ="/room/room";
        },
        error: function() {
            alert("failed to join room");
        }
    });
}

function append_rooms(data) {
    $("#room_container").empty();
    if (data["data"].length == 0) {
        $("#room_container")
            .append('<button class="btn btn-default btn-primary btn-block">Create a Room</button>')
            .click(function(event) {
                event.preventDefault();
                window.location.href ="/room/create";
            });
    } else {
        $.each(data["data"], function(index, value) {
            var button = $($.parseHTML('<button class="btn btn-default btn-primary btn-block">' + value["name"] + '</button>'));
            button.click((function (name) {
                return function() {
                    event.preventDefault();
                    join_room(name);
                }
            })(value["name"]));

            $("#room_container").append(button);
        });
    }
}

function load_rooms() {
    $.ajax({
        url: "/api/room/listrooms",
        success: function(data) {
            append_rooms(data);
        }
    });

    setTimeout(load_rooms, 5000);
}

$(document).ready(function() {
    load_rooms();
});
