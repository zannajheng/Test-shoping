$(function () {
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
            $('#login_user').next('div').html('用户名介于1-20位').show()
            error_name = true;
        } else {
            $.get('/user/login/check', {uname: $('#login_user').val()}, function (data) {
                if (data.count == 1) {
                    $('#login_user').next('div').hide()
                    error_name = false;
                } else {
                    $('#login_user').next('div').html('用户不存在').show()
                    error_name = true;
                }
            })
        }
    }

    function passwod() {
        var len = $('#login_password').val().length;
        if (len < 6 || len > 20) {
            $('#login_password').next('div').html('密码介于6-20位之间').show()
            error_password = true;
        } else {
            $('#login_password').next('div').hide()
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
});

