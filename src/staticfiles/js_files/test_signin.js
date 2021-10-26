$(document).on('submit', '#login_form', function(event) {
    event.preventDefault();

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.ajax({
        type: 'POST',
        url: 'http://0.0.0.0:8083/signin/',
        dataType: "json",
        contentType: "application/json",
        headers: {'X-CSRFToken': csrf_token},
        data: JSON.stringify({
            email:$('#id_email').val(),
            password:$('#id_password').val(),
        }),

        success: function(response) {
            if (response.verify_email) {
                alert(response["verify_email"]);
                $('#verify-email').html("<a href='http://0.0.0.0:8083/get/verification/link/" + $('#id_email').val() + "/'><h2><b>Send me verification link now</b></h2></a>")
            } else if ( response.access_token ) {
                localStorage.setItem('access_token', response["access_token"]);
                localStorage.setItem('refresh_token', response["refresh_token"]);
                console.log("Access token:" + response["access_token"]);
                alert('You have been logged in')
            }
            $('#id_email').val('');  // remove values from form
            $('#id_password').val('');
        },
        error: function(){
           alert('Error - Email or Password is invalid');
        }
    });
});

$('#test-post').click(function(){

    $.ajax({
        type: 'GET',
        url: 'http://0.0.0.0:8083/test-post-create/',
        dataType: "json",
        contentType: "application/json",
        headers: {'Authorization': 'Bearer ' + localStorage.getItem('access_token')},

        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                $("#posts-list").append('<b>' + data[i]['title'] + '</b><br>');
                $("#posts-list").append('Author: <i>' + data[i]['user']['username'] + '</i><br>');
                $("#posts-list").append(data[i]['content'] + '<br><hr>');
            }
        },
        error: function(xhr, status, error){
           var errorMessage = xhr.status + ': ' + xhr.statusText
           alert('Error - ' + errorMessage);
        }
    });
});