"use strict";

function join_room_window(name, pwd_req) {
    $("#room_title").html(name);

    if (pwd_req) {
        $("#join").before('<input id="room_pwd" type="password" placeholder="password" />');
    }

    $("#join").click((function(name) {
        return function() {
            event.preventDefault();
            var data = {};
            data.name = name;
            if ($("#room_pwd").length !== 0) {
                data.password = $("#room_pwd").val();
            }
            join_room(JSON.stringify(data));
        };
    })(name));
    $("#join_room_dialog").modal("show");
}

function join_room(data) {
    $.ajax({
        type: "POST",
        url: "/api/room/joinroom",
        data: data,
        success: function() {
            window.location.href = "/room/lobby";
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
                window.location.href = "/room/create";
            });
    } else {
        $.each(data["data"], function(index, value) {
            var button = $($.parseHTML('<button class="btn btn-default btn-primary btn-block">' + value["name"] + '</button>'));
            button.click((function(name, pwd_req) {
                return function() {
                    event.preventDefault();
                    join_room_window(name, pwd_req);
                }
            })(value["name"], value["pwd_req"]));

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
