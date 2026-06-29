$(document).ready(function () {
$('.title').each(function (){
    var user = $(this).text()
       if (user.length > 2) {
        var maskedUser = user[0] + '*'.repeat(user.length - 2) + user[user.length - 1];
        $(this).text(maskedUser);
    }
})
    $('#more_list_next').click(function (event) {
        event.preventDefault();
        var page = parseInt($(this).siblings('.active').text()) + 1
        var type_id = parseInt($('#type_Id').val())
        $.ajax({
            'url': '/user/index/list/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'type_id': type_id
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods)
                    more_cart()
                    var active = $('.more_list_pagenation .active');
                    var prevaint = parseInt($('#more_list_next').prev('a').text())
                    activeint = active.text()
                    if (activeint == prevaint) {
                        $('.more_list_pagenation a').each(function () {
                            var num = parseInt($(this).text())
                            if (!isNaN(num)) {
                                $(this).text(num + 1);
                            }
                        })
                    }
                    var next = active.next('a');
                    if (next.length > 0 && next.attr('id') !== 'more_list_next') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }  else {
                    Maxpages(response.pages)
                }
            }

        })
    })

    $('#more_list_previous').click(function (event) {
        event.preventDefault();
        var page = parseInt($(this).siblings('.active').text()) - 1
        var type_id = parseInt($('#type_Id').val())
        $.ajax({
            'url': '/user/index/list/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'type_id': type_id
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods)
                    more_cart()
                    var active = $('.more_list_pagenation .active');
                    var activeint = active.text()
                    var previousint = $('#more_list_previous').next('a').text()
                    if (activeint == previousint) {
                        $('.more_list_pagenation a').each(function () {
                            var num = parseInt($(this).text())
                            if (!isNaN(num)) {
                                $(this).text(num - 1)
                            }
                        })
                    }
                    var next = active.prev('a');
                    if (next.length > 0 && next.attr('id') !== 'more_list_previous') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }  else {
                    Maxpages(response.pages)
                }
            }

        })
    })

    $('.more_list_pagenation a').not('#more_list_next', '#more_list_previous').on('click', function (event) {
        event.preventDefault()
        var page = parseInt($(this).text())
        var type_id = parseInt($('#type_Id').val())
        var page_this = this
        $.ajax({
            'url': '/user/index/list/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'type_id': type_id
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods)
                    more_cart()
                    var active = $('.more_list_pagenation .active');
                    $(page_this).addClass('active');
                    active.removeClass('active');
                }  else {
                    Maxpages(response.pages)
                }
            }
        })
    })

    function pageing(data) {
        $li = ''
        for (var i = 0; i < data.length; i++) {
            $li += '<li>' +
                '<a href="' + data[i].intro + '">' +
                '<img src="' + data[i].images + '" >' +
                '</a>' +
                '<h4>' +
                '<a href="' + data[i].intro + '">' + data[i].goods_name +
                '</a>' +
                '</h4>' +
                '<div class="operate">' +
                '<span class="prize">' + '￥' + data[i].price + '</span>' +
                '<span class="unit">' + data[i].price + '/' + data[i].cation + '</span>' +
                '<div class="point"></div>' +
                '<a href="#" class="more_addgoods" sku_id="' + data[i].id + '" title="加入购物车"></a>' +
                '</div>' +
                '<input type="hidden" id="type_Id" value="' + data[i].type_id_id + '">' +
                '</li>'
        }
        $('.goods_type_list').empty().append($li);

    }

    function more_cart() {
        $('.more_addgoods').click(function (event) {
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

    }

    $('#more_list_default').click(function () {
        location.reload();
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

    $('#more_list_price').click(function (event) {
        event.preventDefault()
        var goods_type_id = $('#more_list_type_id').val()
        var $this = $(this)
        var page = 1
        $.ajax({
            'url': '/user/index/list/price/',
            'type': 'GET',
            'data': {
                'type_id': goods_type_id,
                'page': page,

            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods)
                    $div =
                        '<a href="#" id="more_list_price_previous">' + '<上一页' + '</a>' +
                        '<a href="#" class="active">1</a>' +
                        ' <a href="#">2</a>' +
                        '<a href="#">3</a>' +
                        '<a href="#">4</a>' +
                        '<a href="#">5</a>' +
                        ' <a href="#" id="more_list_price_next">下一页></a>'
                    $('.more_list_pagenation').empty().append($div)
                    var active = $('.sort_bar .active')
                    $this.addClass('active')
                    active.removeClass('active')
                    more_cart()
                    more_list_price_pageing()
                }
                else {
                    Maxpages(response.pages)
                }
            }
        })

    })

    function more_list_price_pageing() {
        $('#more_list_price_next').click(function (event) {
            event.preventDefault();
            var page = parseInt($(this).siblings('.active').text()) + 1
            var type_id = $('#more_list_type_id').val()
            $.ajax({
                'url': '/user/index/list/price/',
                'type': 'GET',
                'data': {
                    'page': page,
                    'type_id': type_id
                },
                success: function (response) {
                    if (response.code == 200) {
                        pageing(response.goods)
                        more_cart()
                        var active = $('.more_list_pagenation .active');
                        var next = active.next('a');
                        var axtiveint = active.text()
                        var prevint = $('#more_list_price_next').prev('a').text()
                        if (axtiveint == prevint) {
                            $('.more_list_pagenation a').each(function () {
                                var num = parseInt($(this).text())
                                if (!isNaN(num)) {
                                    $(this).text(num + 1)
                                }
                            })
                        }
                        if (next.length > 0 && next.attr('id') !== 'more_list_price_next') {
                            active.removeClass('active');
                            next.addClass('active');
                        }
                    }
                }

            })
        })
        $('#more_list_price_previous').click(function (event) {
            event.preventDefault();
            var page = parseInt($(this).siblings('.active').text()) - 1
            var type_id = $('#more_list_type_id').val()
            $.ajax({
                'url': '/user/index/list/price/',
                'type': 'GET',
                'data': {
                    'page': page,
                    'type_id': type_id
                },
                success: function (response) {
                    if (response.code == 200) {
                        pageing(response.goods)
                        more_cart()
                        var active = $('.more_list_pagenation .active');
                        var activeint = active.text()
                        var nextint = $('#more_list_price_previous').next('a').text()
                        if (activeint == nextint) {
                            $('.more_list_pagenation a').each(function () {
                                var num = parseInt($(this).text())
                                if (!isNaN(num)) {
                                    $(this).text(num - 1)
                                }
                            })
                        }
                        var next = active.prev('a');
                        if (next.length > 0 && next.attr('id') !== 'more_list_price_previous') {
                            active.removeClass('active');
                            next.addClass('active');
                        }
                    }
                }

            })
        })
        $('.more_list_pagenation a').not('#more_list_price_next', '#more_list_price_previous').on('click', function (event) {
            event.preventDefault()
            var page = parseInt($(this).text())
            var type_id = $('#more_list_type_id').val()
            var page_this = this
            $.ajax({
                'url': '/user/index/list/price/',
                'type': 'GET',
                'data': {
                    'page': page,
                    'type_id': type_id
                },
                success: function (response) {
                    if (response.code == 200) {
                        pageing(response.goods)
                        more_cart()
                        var active = $('.more_list_pagenation .active');
                        $(page_this).addClass('active');
                        active.removeClass('active');
                    }
                }
            })
        })
    }
        function Maxpages(pages){
                      $('.login_message_ajax').css('display', 'block').text(`最多只有${pages}页！`);
            // 重置动画
            $('.login_message_ajax').css('animation', 'none');
            setTimeout(function () {
                $('.login_message_ajax').css('animation', '');
            }, 10);
    }


})
