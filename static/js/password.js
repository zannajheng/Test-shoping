$(function () {
    var password_user = false;
    var password_pw1 = false;
    var password_pw2 = false
    $('#password_user').blur(function () {
        uname()
    })
    $('#password_pw1').blur(function () {
        passwod1()

    })
    $('#password_pw2').blur(function () {
        passwod2()

    })

    function uname() {
        var len = $('#password_user').val().length
        if (len < 1 || len > 20) {
            $('#password_user').next('span').html('用户名介于1-20位').show()
            error_name = true;
        } else {
            $.get('/user/login/check', {uname: $('#password_user').val()}, function (data) {
                if (data.count == 1) {
                    $('#password_user').next('span').hide()
                    error_name = false;
                } else {
                    $('#password_user').next('span').html('用户不存在').show()
                    error_name = true;
                }
            })
        }
    }

    function passwod1() {
        var len = $('#password_pw1').val().length;
        if (len < 6 || len > 20) {
            $('#password_pw1').next('span').html('密码介于6-20位之间').show()
            error_password = true;
        } else {
            $('#password_pw1').next('span').hide()
            error_password = false;
        }
    }

    function passwod2() {
        var pass1 = $('#password_pw1').val()
        var pass2 = $('#password_pw2').val()

        if(pass1 != pass2) {
            $('#password_pw2').next('span').html('两次输入密码不一致').show()
            error_password2 = true;
        }
        else {
            $('#password_pw2').next('span').hide()
            error_password2 = false;
        }

    }

    $('passwordfrom').submit(function (event) {
        uname()
        passwod1()
        passwod2()
        if (password_user == false && password_pw1 == false && password_pw2 == false) {
            return true
        } else {
            event.preventDefault()
            return false;
        }
    })
});
