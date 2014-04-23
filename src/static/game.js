'use strict';

var NUM_BALLS = 15;
var WIDTH_THRESHOLD = 440;
var BALL_GAP = 4.25;

// inner indices of BALL_IDS:
var BALL_STRING = 0;
var BALL_COLOR = 1;

var ID_TO_BALL = {
    'ball-one': 1, 'ball-two': 2, 'ball-three': 3,
    'ball-four': 4, 'ball-five': 5, 'ball-six': 6,
    'ball-seven': 7, 'ball-eight': 8, 'ball-nine': 9,
    'ball-ten': 10, 'ball-eleven': 11, 'ball-twelve': 12,
    'ball-thirteen': 13, 'ball-fourteen': 14, 'ball-fifteen': 15
};

var BALL_IDS = [
    ['ball-one', '#FFD342'],
    ['ball-two', '#0000EC'],
    ['ball-three', '#B90315'],
    ['ball-four', '#650090'],
    ['ball-five', '#F6731B'],
    ['ball-six', '#165F3D'],
    ['ball-seven', '#7F1D1D'],
    ['ball-eight', '#000000'],
    ['ball-nine', '#0000EC'],
    ['ball-ten', '#B90315'],
    ['ball-eleven', '#650090'],
    ['ball-twelve', '#F6731B'],
    ['ball-thirteen', '#165F3D'],
    ['ball-fourteen', '#7F1D1D'],
    ['ball-fifteen', '#000000']
];

$(document).ready(function() {
    load_ball_content();
    setup_triangle_ready();
    get_player_balls();
    on_click_ball();
    load_players();
    leave_game();
});

$(window).resize(function() {
    setup_triangle_ready();
});

function load_ball_content() {
    for(var i = 1; i <= 15; i++) {
        var spanId = '#b' + i.toString();
        var figureId = '#' + BALL_IDS[i-1][BALL_STRING];
        $(spanId).attr('data-content', i.toString());
        $(figureId).css('background',BALL_IDS[i-1][BALL_COLOR]);
    }

}

function setup_triangle_ready() {
    var viewportWidth = $(window).innerWidth();

    if(viewportWidth < WIDTH_THRESHOLD) {
        var diameter =  $('#game_container').width() / 5 - 15;
        $('.ball').css('width', toPixel(diameter));
        $('.ball').css('height', toPixel(diameter));

        var fontSize = Math.round(diameter / 2.5);
        $('.ball').css('font-size', toPixel(fontSize));

        for(var i = 1; i <= 5; i++) {
            var row = '.ball-row-' + i.toString();
            var row_width = diameter * i + BALL_GAP * (i-1);
            $(row).css('width', toPixel(row_width));
            $(row).css('height', toPixel(diameter));
        }
    }
    else {
        var diameter = 55;
        $('.ball').css('width', toPixel(diameter));
        $('.ball').css('height', toPixel(diameter));
        $('.ball').css('font-size', 22);

        for(var i = 1; i <= 5; i++) {
            var row = '.ball-row-' + i.toString();
            var row_width = diameter * i + BALL_GAP * (i-1);
            $(row).css('width', toPixel(row_width));
            $(row).css('height', toPixel(diameter));
        }
    }
}

function toPixel(num) {
    return num.toString() + 'px';
}

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
                $('#' + BALL_IDS[j][BALL_STRING]).css('opacity', 0.3);
            }

            $.each(data.data.balls_on_table, function(key, value) {
                $('#' + BALL_IDS[value-1][BALL_STRING]).css('opacity', 1);
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
    $('.ball').click($.debounce(100, function(event) {
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
        var ball_id = '#' + String(BALL_IDS[v-1][BALL_STRING]);
        $.each(["webkit", "moz"], function(n, i) {
            $(ball_id).css("-" + i + "-animation-iteration-count", "infinite");
        });
        $(ball_id).addClass('animated pulse');
    });
}
