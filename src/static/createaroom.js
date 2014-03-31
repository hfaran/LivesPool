'use strict';

$(document).ready(function() {
    $('#createroomForm').submit(function(event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/api/room/createroom',
            data: JSON.stringify($('#createroomForm').serializeObject()),
            content_type: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function() {
                window.location.href = '/room/lobby';
            },
            error: function(jqXHR, status, error) {
                if (jqXHR.status === 409) {
                    alert('Room already exists');
                }
            }
        });
    });
});
