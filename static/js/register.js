$(document).ready(function () {

    var error_name = false;
    var error_password = false;
    var error_check_password = false;
    var error_email = false;
    var error_check = false;


    $('#user_name').blur(function () {
        check_user_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });

    $('#email').blur(function () {
        check_email();
    });

    $('#allow').click(function () {
        if ($(this).is(':checked')) {
            error_check = false;
            $(this).siblings('span').hide();
        } else {
            error_check = true;
            $(this).siblings('span').html('请勾选同意');
            $(this).siblings('span').show();
        }
    });

    function check_user_name() {
        var len = $('#user_name').val().length;
        if (len < 1 || len > 20) {
            $('#user_name').next().html('请输入1-20个字符的用户名').show()
            error_name = true;
        } else {
            var uname = $('#user_name').val()
            $.ajax({
                url: '/user/register/check',
                type: 'GET',
                data: {
                    'uname': uname,
                },
                success: function (response) {
                    if (response.count == 1) {
                        $('#user_name').next('span').text('用户已存在').show()
                        error_name = true;
                    } else {
                        $('#user_name').next('span').hide()
                        error_name = false;
                    }

                },
                error: function (error) {
                    console.log(error);
                }
            });

        }
    }

    function check_pwd() {
        var len = $('#pwd').val().length;
        var cpwd = $("#cpwd").val()
        var pwd = $('#pwd').val()
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位').show();
            error_password = true;
        } else {
            $('#pwd').next().hide();
            error_password = false;
        }
        if (cpwd) {
            if (cpwd != pwd) {
                $('#cpwd').next().html('两次输入的密码不一致').show();
                error_check_password = true;
            }
            else {
                  $('#cpwd').next().hide();
            error_check_password = false;
            }
        }
    }

    function check_cpwd() {
        var pass = $('#pwd').val();
        var cpass = $('#cpwd').val();

        if (pass != cpass) {
            $('#cpwd').next().html('两次输入的密码不一致').show();
            error_check_password = true;
        } else {
            $('#cpwd').next().hide();
            error_check_password = false;
        }

    }

    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if ($('#email').val() == '' || re.test($('#email').val())) {
            $('#email').next().hide();
            error_email = false;
        } else {
            $('#email').next().html('你输入的邮箱格式不正确')
            $('#email').next().show();
            error_check_password = true;
        }

    }


    $('#button').click(function () {

        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();
        if (error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false) {
            var user = $('#user_name').val()
            var password = $('#pwd').val()
            var password_confirmation = $('#cpwd').val()
           $.ajax({
               url: '/user/register/sumbit/',
               type: 'POST',
               data: {
                   'user': user,
                   'password': password,
                   'password_confirmation': password_confirmation,
               },
               success: function (response){
                   if (response.code == 200){
                        window.location.href = 'http://127.0.0.1:8000/user/login/'
                   }else {
                         $('#user_name').next().html(response.message).show()
                            error_name = true;
                   }
               },
               error: function (e){
                   console.log(e)

               }
           })
        }
    })

})
