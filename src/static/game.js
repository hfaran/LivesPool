'use strict';

var NUM_BALLS = 15;

var ID_TO_BALL = {
    'ball-one': 1, 'ball-two': 2, 'ball-three': 3,
    'ball-four': 4, 'ball-five': 5, 'ball-six': 6,
    'ball-seven': 7, 'ball-eight': 8, 'ball-nine': 9,
    'ball-ten': 10, 'ball-eleven': 11, 'ball-twelve': 12,
    'ball-thirteen': 13, 'ball-fourteen': 14, 'ball-fifteen': 15
};

var BALL_IDS = [
    'ball-one', 'ball-two', 'ball-three',
    'ball-four', 'ball-five', 'ball-six',
    'ball-seven', 'ball-eight', 'ball-nine',
    'ball-ten', 'ball-eleven', 'ball-twelve',
    'ball-thirteen', 'ball-fourteen','ball-fifteen'
];

$(document).ready(function() {
    get_player_balls();
    on_click_ball();
    load_players(); // TODO: fix player list layout
    leave_game();
});

function get_player_balls() {
    // Puts player_balls in sessionStorage so that highlight_player_balls
    //  may use it later
    $.ajax({
        url: '/api/player/player',
        success: function(data) {
            sessionStorage.clear();
            sessionStorage.setItem('player_balls', JSON.stringify(data.data.orig_balls));
        }
    }).done(function() {
        load_balls();
    });
}

function load_balls() {
    $.ajax({
        url: '/api/game/gamestate',
        success: function(data) {
            for(var j = 0; j < NUM_BALLS; j++) {
                $('#' + BALL_IDS[j]).css('opacity', 0.3);
            }

            $.each(data.data.balls_on_table, function(key, value) {
                $('#' + BALL_IDS[value-1]).css('opacity', 1);
            });

            if(data.data.winner != "") {
                $.ajax({
                    url: '/api/game/endgame',
                    type: 'DELETE',
                    success: function() {
                        alert('The winner is: ' + data.data.winner);
                        window.location.href = '/';
                    }
                });
            }
        }
    }).done(function() {
        highlight_player_balls();
    });
    setTimeout(load_balls, 5000);
}

function on_click_ball() {
    $('div.poolball').click($.debounce(100, function(event) {
        var id = $(this).attr('id');
        toggle_ball(id, this);
    }));
}

function toggle_ball(id, div) {
    var num = ID_TO_BALL[id];

    $.ajax({
        type: 'POST',
        url: '/api/game/toggleball',
        data: JSON.stringify({ball: num}),
        success: function() {
            console.log('Successful POST: ball #' + (num));
        }
    }).done(function() {
        if($(div).css('opacity') == 1) {
            $(div).fadeTo(700, 0.3);
        }
        else {
            $(div).fadeTo(700, 1);
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

function highlight_player_balls() {
    var player_balls = JSON.parse(sessionStorage.getItem('player_balls'));

    $.each(player_balls, function(k, v) {
        var ball_id = '#' + String(BALL_IDS[v-1]);
        $.each(["webkit", "moz"], function(n, i) {
            $(ball_id).css("-" + i + "-animation-iteration-count", "infinite");
        });
        $(ball_id).addClass('animated pulse');
    });
}
