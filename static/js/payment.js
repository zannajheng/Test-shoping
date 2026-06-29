$(document).ready(function () {
    $('#order_btn').click(function () {
        setTimeout(function () {
            var selectedPayment = $('input[type=radio][name=pay_style]:checked').next().text();
            if (selectedPayment != '支付宝支付') {
                $('.login_message_ajax').css('display', 'block').text('只支持支付宝付款！');
            // 重置动画
            $('.login_message_ajax').css('animation', 'none');
            setTimeout(function () {
                $('.login_message_ajax').css('animation', '');
            }, 10);
            return
            } else {
                var order_number = $('#order_number').val()
                $.ajax({
                    'url': '/user/order/payment',
                    'type': 'GET',
                    'data': {
                        'order_number': order_number
                    },
                    success: function (response) {
                        if (response.code == 200) {
                            window.location.href = response.alipay_url;
                        }
                    }
                })
            }
        }, 100);


    })
})