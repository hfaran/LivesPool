'use strict';


var indexToId = [
    'placeholder',
    'ball-one',
    'ball-two',
    'ball-three',
    'ball-four',
    'ball-five',
    'ball-six',
    'ball-seven',
    'ball-eight',
    'ball-nine',
    'ball-ten',
    'ball-eleven',
    'ball-twelve',
    'ball-thirteen',
    'ball-fourteen',
    'ball-fifteen'
];


function highlight_player_balls() {

    /* Store player_balls in localStorage so we don't have
    to fetch it every second*/
    if (localStorage.getItem('player_balls') === null || localStorage.getItem('pb_refresh_count') > 5) {
        $.ajax({
            url: '/api/player/player',
            success: function(data) {
                localStorage.setItem('player_balls', JSON.stringify(data.data.orig_balls));
            }
        });
        localStorage.setItem('pb_refresh_count', '0');
    }
    else {
        var pb_refresh_count = Number(localStorage.getItem('pb_refresh_count'));
        localStorage.setItem('pb_refresh_count', String(pb_refresh_count + 1));
    }
    var player_balls = JSON.parse(localStorage.getItem('player_balls'));

    // Swap background-color with color to create crappy flashing effect
    // TODO: Make this less crappy
    $.each(player_balls, function(k, v) {
        var ball_id = '#' + String(indexToId[v]);
        var bgc = $(ball_id).css('background-color');
        var c = $(ball_id).css('color');
        $(ball_id).css('background-color', c);
        $(ball_id).css('color', bgc);
    });

    // This happens every second
    setTimeout(highlight_player_balls, 1000);
}


function load_balls() {
    var ballsInPlay = {
        'placeholder': false,
        'ball-one': false,
        'ball-two': false,
        'ball-three': false,
        'ball-four': false,
        'ball-five': false,
        'ball-six': false,
        'ball-seven': false,
        'ball-eight': false,
        'ball-nine': false,
        'ball-ten': false,
        'ball-eleven': false,
        'ball-twelve': false,
        'ball-thirteen': false,
        'ball-fourteen': false,
        'ball-fifteen': false
    };

    $.ajax({
        url: '/api/game/gamestate',
        success: function(data) {
            $.each(data.data.balls_on_table, function(index, value) {
                ballsInPlay[indexToId[value]] = true;
            });
            $.each(ballsInPlay, function(index, value) {
                if (value) {
                    $('#' + index).css('opacity', 1);
                } else {
                    $('#' + index).css('opacity', 0.3);
                }
            });
        }
    });

    setTimeout(load_balls, 5000);
    return ballsInPlay;
}


function toggle_ball(id) {
    var idToBall = {
        'ball-one': 1,
        'ball-two': 2,
        'ball-three': 3,
        'ball-four': 4,
        'ball-five': 5,
        'ball-six': 6,
        'ball-seven': 7,
        'ball-eight': 8,
        'ball-nine': 9,
        'ball-ten': 10,
        'ball-eleven': 11,
        'ball-twelve': 12,
        'ball-thirteen': 13,
        'ball-fourteen': 14,
        'ball-fifteen': 15
    };

    var num = idToBall[id];

    $.ajax({
        type: 'POST',
        url: '/api/game/toggleball',
        data: JSON.stringify({
            ball: num
        }),
        success: function() {
            console.log('Successful POST: ball #' + num);
        }
    });
}


function on_click_ball(ballsInPlay) {
    $('div.poolball').click(function() {
        var id = $(this).attr('id');
        if (ballsInPlay[id]) {
            $(this).fadeTo(700, 0.3);
            ballsInPlay[id] = false;
            toggle_ball(id);
        } else {
            $(this).fadeTo(700, 1);
            ballsInPlay[id] = true;
            toggle_ball(id);
        }
    });
}


function load_players() {
    $.ajax({
        url: '/api/game/listplayers',
        success: function(data) {
            $('#game_list').empty();
            $('#game_list').append('<ul id="playerlist" ' +
                'class="list-group"></ul>');

            var firstItem = true;
            $.each(data.data.players, function(key, value) {

                if (firstItem) {
                    $('ul#playerlist').append('<li ' +
                        'class="list-group-item owner">' + value + '</li>');
                    firstItem = false;
                } else {
                    $('ul#playerlist').append('<li ' +
                        'class="list-group-item">' + value + '</li>');
                }
            });
        }
    });
}


function leave_game() {
    $('#leavegamebutton').click(function() {
        $.ajax({
            url: '/api/game/leavegame',
            type: 'DELETE',
            success: function() {
                window.location.href = '/room/join';
            }
        });
    });
}


$(document).ready(function() {
    var ballsInPlay = load_balls();
    on_click_ball(ballsInPlay);
    load_players(); // TODO: fix player list layout
    leave_game();
    highlight_player_balls();
});
