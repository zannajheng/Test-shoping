$(document).ready(function () {
    var query = $('#search_a').text()
    $('.serach_li').each(function () {
        var text = $(this).text()
        var regex = new RegExp(query, "gi");
        var highlightedText = text.replace(regex, '<span class="highlight">' + query + '</span>');
        $(this).html(highlightedText);
    })


    $('#seleect_all').click(function () {
        $('.seleect').prop('checked', this.checked);
    });
    $('.seleect').on('change', function () {
        var total = $('.seleect').length;
        var checked = $('.seleect:checked').length;
        if (total == checked) {
            $('#seleect_all').prop('checked', true);
        } else {
            $('#seleect_all').prop('checked', false);
        }
    });
    $('.seleect, #seleect_all').change(function () {
        var selectedCount = $('.seleect:checked').length;
        $('#countsum').text(selectedCount)
    });

    $('#cart_add').click(function () {
        var num_show = parseInt($('#cart_num').val())
        $('#cart_num').val(num_show + 1)
        total()
    })
    $('#cart_decr').click(function () {
        var num_show = parseInt($('#cart_num').val())
        if (num_show > 1) {
            $('#cart_num').val(num_show - 1)
            total()
        }
    })

    function total() {
        var price = parseFloat($('#unit').text())
        var num = parseInt($('#cart_num').val())
        var to = (price * num).toFixed(2)
        $('#total').text(to)
    }

    $('#add_cart').click(function () {
        var sku_id = $(this).attr('sku_id')
        var num_show = parseInt($('#cart_num').val())
        var csrf_token = $('#csrf-token  input').val();
        $.ajax({
            url: '/user/cartadd/',
            type: 'POST',
            data: {
                sku_id: sku_id,
                num_show: num_show,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (response) {
                if (response.code == 200) {
                    posion(response.count)
                    alert("加入购物车成功")
                } else {
                    window.location.href = '/user/login/?is_login=' + 'notlogin';
                }


            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText)
            }
        })
    })
    $('.search_cart_add, .more_addgoods').click(function (event) {
        event.preventDefault();
        var sku_id = $(this).attr('sku_id')
        var csrf_token = $('#csrf-token input').val()
        var $bt = $(this)
        var $point = $(this).siblings('.point');
        $.ajax({
            url: '/user/search/cartadd/',
            type: 'POST',
            data: {
                sku_id: sku_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {
                posion_search(response.count, $point, $bt)

            }
        })

    })

    function posion_search(count, $point, $bt) {
        var $car = $('#car')
        var $pos = $bt.offset()
        var $carpos = $car.offset()
        $point.css({'left': $pos.left + $bt.outerWidth() / 2 - 5, 'top': $pos.top + $bt.outerHeight() / 2 - 5})
        $point.show()
        $point.stop().animate({
            'left': $carpos.left + $car.outerWidth() / 2 - 5,
            'top': $carpos.top + $car.outerHeight() / 2 - 5
        }, 1000, function () {
            $point.hide()
            $('#show_count').text(count);
        })
    }

    function posion(count) {
        $('#show_count').text(count);
        /* var $car = $('#car')
         var $bt = $('#add_cart')
         var $point = $('.point')
         var $pos = $bt.offset()
         var $carpos = $car.offset()
         $point.css({'left': $pos.left + $bt.outerWidth() / 2 - 5, 'top': $pos.top + $bt.outerHeight() / 2 - 5})
         $point.show()
         $point.stop().animate({
             'left': $carpos.left + $car.outerWidth() / 2 - 5,
             'top': $carpos.top + $car.outerHeight() / 2 - 5
         }, 1000, function () {
             $point.hide()
             $('#show_count').text(count);
         })*/

    }

    $('.add').click(function () {
        var sku_id = $(this).attr('sku_id')
        var csrf_token = $('#csrf-token input').val()
        var num_show = parseInt($(`input[sku_id="${sku_id}"]`).val())
        $.ajax({
            url: '/user/cart/add/',
            type: 'POST',
            data: {
                sku_id: sku_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {
                $(`input[sku_id="${sku_id}"]`).val(num_show + 1)
                update_show(sku_id)
            }
        })

    })
    $('.minus').click(function () {
        var sku_id = $(this).attr('sku_id')
        var csrf_token = $('#csrf-token input').val()
        var num_show = parseInt($(`input[sku_id="${sku_id}"]`).val())
        if (num_show > 1) {
            $.ajax({
                url: '/user/cart/decr/',
                type: 'POST',
                data: {
                    sku_id: sku_id,
                    csrfmiddlewaretoken: csrf_token,
                },
                success: function (response) {
                    $(`input[sku_id="${sku_id}"]`).val(num_show - 1)
                    update_show(sku_id)
                }
            })
        }
    })

    function update_show(sku_id) {
        var price = parseFloat($('li.col05[sku_id="' + sku_id + '"]').text());
        var num_show = parseInt($(`input[sku_id="${sku_id}"]`).val())
        var toprice = (price * num_show).toFixed(2)
        $('li.col07[sku_id="' + sku_id + '"]').text(toprice);
        var total = 0
        $('li.col07').each(function () {
            total += parseFloat($(this).text())
        })
        $('#totalsum').text(total.toFixed(2));
    }

    $('a.codelete').click(function () {
        if (confirm("确定要删除吗？")) {
            var sku_id = $(this).attr('sku_id')
            var csrf_token = $('#csrf-token input').val()
            $.ajax({
                url: '/user/cart/delete/',
                type: 'POST',
                data: {
                    sku_id: sku_id,
                    csrfmiddlewaretoken: csrf_token,
                },
                success: function (response) {
                    $(`ul[sku_id="${sku_id}"]`).remove()
                    update_show()
                    $('ul.cart_list_td').each(function (index) {
                        // $(this).find('li.col01').text(index + 1 + '.');
                        $(this).find('li.col01').html('<input type="checkbox" class="seleect" checked>&nbsp;' + (index + 1) + '.');
                        bindEvents()

                    });
                    var countsum = parseInt($('#countsum').text())
                    $('#countsum').text(countsum - 1)
                    var show_count = parseInt($('#show_count').text())
                    $('#show_count').text(show_count - 1)
                    var allitem = parseInt($('#allitem').text())
                    $('#allitem').text(allitem - 1)


                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }

            })
        }

    })

    $('#settle').click(function () {
        var addr = $('#addr').val();
        var tel = $('#tel').val();
        if (!addr) {
            alert('请输入收货地址');
            return;
        }
        if (!tel) {
            alert('请输入手机号');
            return;
        }
        var overlay = $('<div id="overlay"></div>').css({
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'background-color': 'rgba(0, 0, 0, 0.5)',
            'z-index': 9998
        });
        $('body').append(overlay);
        $('#toast').show();// 将覆盖层添加到body元素
        $('#toast').css({'display': 'flex', 'z-index': 9999});
        var csrf_token = $('#csrf-token input').val()

        var goods = [];
        $('.seleect:checked').each(function () {
            var sku_id = $(this).closest('ul').attr('sku_id');
            var count = $(this).closest('ul').find('.num_show').val();
            goods.push({
                sku_id: sku_id,
                count: count,
                addr: addr,
                tel: tel
            });
        });

        $.ajax({
            url: '/user/cart/',
            type: 'POST',
            data: JSON.stringify({
                goods: goods,
            }),
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (response) {
                $('#overlay').remove();
                $('#toast').css('display', 'none');
                $('#toastmenet').css({'display': 'flex', 'z-index': 9999});
                window.location.href = '/user/order';
            }
        })
    })

    $('.add_goods').click(function (event) {
        event.preventDefault();
        var sku_id = $(this).attr('sku_id')
        var csrf_token = $('#csrf-token input').val()
        var $bt = $(this)
        var $point = $(this).siblings('.point');
        $.ajax({
            url: '/user/search/cartadd/',
            type: 'POST',
            data: {
                sku_id: sku_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {
                posion_search(response.count, $point, $bt)

            }
        })
    })

    $('.order_delete').click(function (event) {
        event.preventDefault()
        if (confirm('确定要删除吗？')) {
            order_number = $(this).attr('order_number')
            window.location.href = '/user/order/delete/' + '?order_number=' + order_number
        }
    })

    $('#buy_btn').click(function (e) {
        e.preventDefault()
        var sku_id = $('#add_cart').attr('sku_id')
        var count = $('#cart_num').val()
        var csrf_token = $('#csrf-token input').val()
        $.ajax({
            'url': '/user/index/detail/buy/',
            'type': 'post',
            'data': {
                'sku_id': sku_id,
                'count': count,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {

                if (response.code == 200) {
                    var order_number = response.order_number
                    window.location.href = 'http://127.0.0.1:8000/user/order/payment/' + order_number + '/'
                } else {
                    window.location.href = '/user/login/';
                }
            }
        })
    })

})


function bindEvents() {
    $('#seleect_all').off('click').on('click', function () {
        $('.seleect').prop('checked', this.checked);
    });

    $(document).on('change', '.seleect', function () {
        var total = $('.seleect').length;
        var checked = $('.seleect:checked').length;
        if (total == checked) {
            $('#seleect_all').prop('checked', true);
        } else {
            $('#seleect_all').prop('checked', false);
        }
    });

    $('.seleect, #seleect_all').off('change').on('change', function () {
        var selectedCount = $('.seleect:checked').length;
        $('#countsum').text(selectedCount)
    });
}



