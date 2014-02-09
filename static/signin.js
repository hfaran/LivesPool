$(document).ready(function() {
    $("#signinForm").submit(function(event) {
        event.preventDefault();

        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: JSON.stringify($("#signinForm").serializeObject()),
            content_type: "application/json; charset=utf-8",
            dataType: "json",
            success: function() {
                window.location.href ="/views/room/join";
            },
            error: function() {
                //TODO: callback error handling
                alert("failed to post");
            }
        });
    });

    $("#signinButton").click(function(event) {
        event.preventDefault();
        $("#signinForm").attr("action", "/api/auth/login");
        $("#signinForm").submit();
    });

    $("#signupButton").click(function(event) {
        event.preventDefault();
        $("#signinForm").attr("action", "/api/player/player");
        $("#signinForm").submit();
    });
});
