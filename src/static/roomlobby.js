'use strict';

$(document).ready(function() {
    var initialLoad = true;

    load_players(initialLoad);
    check_start();
});

function load_players(initialLoad) {
    var gamemaster;
    $.ajax({
        url: '/api/room/listplayers',
        success: function(data) {
            $('#lobby_container').empty();
            $('#lobby_container').append('<ul id="playerlist" ' +
                'class="list-group"></ul>');

            var firstItem = true;
            $.each(data.data.players, function(key, value) {

                if (firstItem) {
                    $('ul#playerlist').append('<li class="list-' +
                        'group-item owner">' + value + '</li>');
                    firstItem = false;
                    gamemaster = value.toString();
                } else {
                    $('ul#playerlist').append('<li class="list-' +
                        'group-item">' + value + '</li>');
                }

            });
        }
    }).done(function() {
        // only call load_buttons once
        if(initialLoad !== undefined) {
            load_buttons(gamemaster);
            initialLoad = undefined;
        }
    });

    setTimeout(load_players, 5000);
}

function load_buttons(gamemaster) {
    $.ajax({
        url: '/api/player/player',
        success: function(data) {
            $('#numBallsForm').empty();
            if(data.data.name == gamemaster.toString()) {
                $('#numBallsForm').append(
                    '<div class="form-group">' +
                        '<label id="ballsPerPlayerLabel" for="inputNumBalls">Balls per player:</label>' +
                        '<div class="form-group">' +
                            '<input id="inputNumBalls" name="nbpp" class="form-control form-spacing numBalls" type="number" required="" max="5" min="1" />' +
                        '</div>' +
                        '<div id="roomlobby-buttons" class="contain-buttons">' +
                            '<button id="leaveroombutton" type="button" class="btn btn-danger btn-block">Leave</button>' +
                            '<button id="startgamebutton" type="submit" class="btn btn-info btn-block">Start</button>' +
                        '</div>' +
                    '</div>'
                );

            }
            else {
                $('#numBallsForm').append(
                    '<div id="roomlobby-buttons" class="contain-buttons">' +
                        '<button id="leaveroombutton" type="button" class="btn btn-danger btn-block">Leave</button>' +
                    '</div>'
                );
            }
        }
    }).done(function() {
        leave_room();
        create_game();
    });
}

function leave_room() {
    $('#leaveroombutton').click(function() {
        $.ajax({
            url: '/api/room/leaveroom',
            type: 'DELETE',
            success: function() {
                window.location.href = '/room/join';
            }
        });
    });
}

function create_game() {
    $('#numBallsForm').submit(function(event) {
        event.preventDefault();

        var num = parseInt($('#inputNumBalls').val());

        $.ajax({
            type: 'POST',
            url: '/api/game/creategame',
            data: JSON.stringify({
                nbpp: num
            }),
            content_type: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function() {
                window.location.href = '/room/game';
            },
            error: function(jqXHR, status, error) {
                // TODO: implement
            }
        });
    });
}

// Forward player to game room if gamemaster has
// started the game
function check_start() {
    $.ajax({
        url: '/api/player/player',
        type: 'GET',
        success: function(data) {
            if (data.data.current_game_id) {
                window.location.href = '/room/game';
            }
        }
    });

    setTimeout(check_start, 5000);
}

