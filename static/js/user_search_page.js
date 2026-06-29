$(document).ready(function () {
    $('#next').click(function (event) {
        event.preventDefault()
        var page = parseInt($('.active').text()) + 1
        var query = $('#search_a').text()
        $.ajax({
            'url': '/user/search/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'query': query
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods_data)
                    var active = $('.pagenation .active');
                    var next = active.next('a');
                    if (next.length > 0 && next.attr('id') !== 'next') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }else {
              Maxpages(response.pages)
                }
            }

        })
    })

    $('#previous').click(function (event) {
        event.preventDefault()
        var page = parseInt($('.active').text()) - 1
        var query = $('#search_a').text()
        $.ajax({
            'url': '/user/search/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'query': query
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods_data)
                    var active = $('.pagenation .active');
                    var next = active.prev('a');
                    if (next.length > 0 && next.attr('id') !== 'previous') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }else {
              Maxpages(response.pages)
                }
            }

        })
    })
    $('.pagenation a').not('#next', '#previous').on('click', function (event) {
        event.preventDefault()
        var page = parseInt($(this).text())
        var query = $('#search_a').text()
        var page_this = $(this)
        $.ajax({
            'url': '/user/search/page/',
            'type': 'GET',
            'data': {
                'page': page,
                'query': query
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response.goods_data)
                    var active = $('.pagenation .active')
                    $(page_this).addClass('active')
                    active.removeClass('active')
                }else {
              Maxpages(response.pages)
                }
            }
        })

    })

    function pageing(data) {
        var $li = ''
        for (var i = 0; i < data.length; i++) {
            $li += '<li>' +
                '<a href="' + data[i].intro + '" >' + '<img src="' + data[i].images + '">' + '</a>' +
                '<h4>' + '<a class="serach_li" href="' + data[i].intro + '">' + data[i].goods_name + '</a>' + '</h4>' +
                '<div class="operate">' +
                '<span class="prize">' + '￥' + data[i].price + '</span>' +
                '<span class="unit">' + data[i].price + '/' + data[i].cation + '</span>' +
                '<div class="point"></div>' +
                '</div>' +
                '<a href="#" class="search_cart_add" sku_id="' + data[i].id + '" title="加入购物车"></a>' +
                '</li>'
        }
        $('.goods_type_list').empty().append($li)
        search_text()
    }

    function search_text() {
        var query = $('#search_a').text()
        $('.serach_li').each(function () {
            var text = $(this).text()
            var regex = new RegExp(query, "gi");
            var highlightedText = text.replace(regex, '<span class="highlight">' + query + '</span>');
            $(this).html(highlightedText);
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