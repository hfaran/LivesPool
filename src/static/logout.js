'use strict';

$(document).ready(function() {
    if (window.location.pathname !== '/signin/signin') {
        $('#afterLogoutItem').after('<li><a id="signoutButton">' +
            'Sign Out</a></li>');
    }

    $('a#signoutButton').click(function() {
        event.preventDefault();

        $.ajax({
            url: '/api/auth/logout',
            type: 'DELETE',
            success: function() {
                window.location.href = '/signin/signin';
            }
        });
    });
});
