$(document).ready(function () {
    $('#next').click(function () {
        var page = parseInt($('.active').text()) + 1
        $.ajax({
            'url': '/user/search/page_next/',
            'type': 'GET',
            'data': {
                'page': page,
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response)
                    var active = $('.pagenation .active');
                    var next = active.next('a');
                    if (next.length > 0 && next.attr('id') !== 'next') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }
                else {

                }
            }

        })
    })
    $('#previous').click(function () {
        var page = parseInt($('.active').text()) - 1
        $.ajax({
            'url': '/admin/index/page_next',
            'type': 'GET',
            'data': {
                'page': page,
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response)
                    var active = $('.pagenation .active');
                    var next = active.prev('a');
                    if (next.length > 0 && next.attr('id') !== 'previous') {
                        active.removeClass('active');
                        next.addClass('active');
                    }
                }
            }

        })
    })

    $('.pagenation a').not('#next', '#previous').on('click', function (){
        var page = parseInt($(this).text())
        var page_this = this
        $.ajax({
            'url': '/admin/index/page_next',
            'type': 'GET',
            'data': {
                'page': page,
            },
            success: function (response) {
                if (response.code == 200) {
                    pageing(response)
                    var active = $('.pagenation .active');
                    $(page_this).addClass('active');
                    active.removeClass('active');
                }
            }
        })
    })

    function pageing(response){
        var $tr = ''
        for (var i = 0; i < response.data.length; i++) {
            $tr += '<tr>' +
                '<td>' + response.data[i].id + '</td>' +
                '<td>' + response.data[i].goods_name + '</td>' +
                '<td><p>' + response.data[i].intro + '</p></td>' +
                '<td>' + response.data[i].price + '</td>' +
                '<td>' + response.data[i].cation + '</td>' +
                '<td>' + response.data[i].sell + '</td>' +
                '<td><img src="' + response.data[i].image_url + '"></td>' +
                '<td>' + response.data[i].goods_type + '</td>' +
                '<td> <span class="edit"><a href="' + response.data[i].edit_url + '">编辑</a></span><span class="delete"><a href="' + response.data[i].delete + '">删除</a></span> </td>'+
                '</tr>'
        }
        $('#tobody').empty().append($tr);

    }

    
})
