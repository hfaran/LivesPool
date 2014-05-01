/* global CryptoJS */

'use strict';

$(document).ready(function() {
    $('#signinForm').submit(function(event) {
        event.preventDefault();

        var data = $('#signinForm').serializeObject();
        if (data.password.length < 4) {
            alert('Password must be at least 4 characters long.');
            return;
        }
        // Hash the password as suggested here:
        //   https://github.com/hfaran/LivesPool/issues/14
        data.password = String(CryptoJS.SHA512(data.password +
            data.username + 'LivesPool'));

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: JSON.stringify(data),
            content_type: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function() {
                window.location.href = '/';
            },
            error: function(jqXHR, status, error) {
                if (jqXHR.status === 400) {
                    alert('Bad username/password combination');
                }
            }
        });
    });

    $('#signinButton').click(function(event) {
        event.preventDefault();
        $('#signinForm').attr('action', '/api/auth/login');
        $('#signinForm').submit();
    });

    $('#signupButton').click(function(event) {
        event.preventDefault();
        $('#signinForm').attr('action', '/api/player/player');
        $('#signinForm').submit();
    });

    $('li#createRoom').remove();
    $('li#joinRoom').remove();
    $('li#about').after('<li><a href="#">Blog</a></li>');
});
