$(document).ready(function () {
    var error_name = false;
    var error_password = false;
    $('#login_user').blur(function () {
        uname()
    })
    $('#login_password').blur(function () {
        passwod()

    })

    function uname() {
        var len = $('#login_user').val().length
        if (len < 1 || len > 20) {
            $('#login_user').next('span').html('用户名为空').show()
            $('#login_user').next('span').css({
                'display':'block',
            });
            error_name = true;
        } else {
            $.ajax({
                'url': '/user/login/check',
                'type': 'GET',
                'data': {
                    'uname': $('#login_user').val()
                },
                success: function (response) {
                    if (response.count == 1) {
                        $('#login_user').next('span').hide()

                        error_name = false;
                    } else {
                        $('#login_user').next('span').html('用户不存在').show()
                        $('#login_user').next('span').css('display', 'block');
                        error_name = true;
                    }

                }
            })
        }

    }


    function passwod() {
        var len = $('#login_password').val().length;
        if (len < 6 || len > 20) {
            $('#login_password').next('span').html('密码介于6-20位之间').show()
            $('#login_user').next('span').css({
                'display':'block',
                'margin-right': '0'
            });
            error_password = true;
        } else {
            $('#login_password').next('span').hide()
            error_password = false;
        }
    }

    $('loginfrom').submit(function (event) {
        uname()
        passwod()
        if (error_name == false && error_password == false) {
            return true
        } else {
            event.preventDefault()
            return false;
        }
    })
    $('#verifycode').on('click', function() {
        $(this).attr('src', "/user/verify/code/?t=" + Math.random());
    });
})


