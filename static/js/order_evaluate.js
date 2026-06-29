$(document).ready(function () {
    $('#order_evaluate_sumbit').click(function () {
        var reviews = [];
        $('.site_con').each(function () {
            var sku_id = $(this).find('input[name="sku_id"]').val();
            var evaluate = $(this).find('textarea[name="evaluate"]').val();

            reviews.push({
                sku_id: sku_id,
                evaluate: evaluate
            });
        });
         var order_number = $("#order_number").val()
        var crsf_token = $('input[name="csrfmiddlewaretoken"]').val()
        console.log(reviews);
        $.ajax({
                    'url': '/user/order/evalute/submit/',
                    'type': 'POST',
                    'data': {
                        'order_number': order_number,
                           'reviews': JSON.stringify(reviews),
                        csrfmiddlewaretoken: crsf_token,

                    },
            success: function (response){
                if (response.code == 200){
                   window.location.href='http://127.0.0.1:8000/user/order/';
                }
            }
    })
})
    });