$(function () {
        const textarea = document.getElementById('txt_input');

const sendButton = document.getElementById('send');
// 监听输入内容变化
        textarea.addEventListener('input', function () {
            // 如果 textarea 有内容
            if (textarea.value.trim() !== '') {
                sendButton.disabled = false; // 启用按钮
            } else {
                sendButton.disabled = true; // 禁用按钮
            }
        });

        onclickimg()
        var now = new Date();
        var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        var thisMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay() + 1);

        // 定义星期数组
        var weekdays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];

        // 初始化前一个日期和时间
        var prevDateTime = null;

        $('.datetime').each(function () {
            // 获取当前元素的日期和时间
            var dateTimeStr = $(this).text();
            var dateTimeParts = dateTimeStr.split(" ");
            var dateParts = dateTimeParts[0].replace("年", "/").replace("月", "/").replace("日", "").split("/");
            var timeParts = dateTimeParts[1].split(":");
            var currentDateTime = new Date(dateParts[0], dateParts[1] - 1, dateParts[2], timeParts[0], timeParts[1]);

            // 检查当前日期和时间与前一个日期和时间的间隔是否大于1分钟
            if (prevDateTime && (currentDateTime - prevDateTime <= 60000)) {
                $(this).text('');
            } else {
                // 检查当前日期是否在本周一之后，如果是，检查是否在今天，如果是，显示时间，否则显示星期几和时间
                if (currentDateTime >= thisMonday) {
                    if (currentDateTime >= today) {
                        $(this).text(dateTimeParts[1]);
                    } else {
                        $(this).text(weekdays[currentDateTime.getDay()] + " " + dateTimeParts[1]);
                    }
                }
            }

            // 更新前一个日期和时间
            prevDateTime = currentDateTime;
        });
        setTimeout(function () {
            var element = $('.raigth_body');
            element.animate({scrollTop: element.prop('scrollHeight')}, 1500);
        }, 1);
        var service = $('.user_service:first a').attr('href').split('=')[1];
        var socket = new WebSocket("ws://localhost:8000/room/" + service + '/')
        socket.onopen = function (even) {
            console.log('链接成功')
        }

        $("#send").click(function () {
            let text = $('#txt_input').val()
            let username = 'admin'
            let message = {
                "username": username, "text": text, "type": 'text'
            };
            // $('#txt_input').val('').focus()
            if (text && text.trim() !== '') {
                socket.send(JSON.stringify(message));
                clearTextarea()
            }


        })
        $("#txt_input").keypress(function (e) {
            if (e.which == 13) {
                e.preventDefault()// 13 是 Enter 键的键值
                $("#send").click(); // 触发点击事件
            }
        });
        socket.onmessage = function (event) {
            updata_reading(event)
            var now = new Date();
            var hours = now.getHours();
            var minutes = now.getMinutes();
            if (hours < 10) {
                hours = '0' + hours;
            }
            if (minutes < 10) {
                minutes = '0' + minutes;
            }
            var time = hours + ':' + minutes;
            var up_time
            $('.datetime').each(function () {
                var text = $(this).text()
                if (text) up_time = text
            })
            if (time == up_time) time = ''
            data = JSON.parse(event.data)
            console.log(data)
            if (data.username == 'admin') {
                if (data.type === 'text') {
                    $div = '<div class="datetime">' + time + '</div>' + '<div class="raigth_div">' + '<p>' + data.text + '</p>' + '</div>'
                } else if (data.type === 'face') {
                    $div = '<div class="datetime">' + time + '</div>' + '<div class="raigth_div">' + '<p>' + '<img style="width: 18px; height: 18px" class="Emoji" src="http://127.0.0.1:8000/static/face/' + data.id + '.png" alt="" />' + '</p>' + '</div>'
                } else {

                    $div = '<div class="datetime">' + time + '</div>' + '<div class="raigth_div">'
                        + '<img src="' + data.image_data + '" class="clickable-img">'
                        + '</div>'
                }

            } else {
                if (data.type === 'text') {
                    $div = '<div class="datetime">' + time + '</div>' + '<div class="line_div">' + '<p>' + data.text + '</p>' + '</div>'
                } else if (data.type === 'face') {
                    $div = '<div class="datetime">' + time + '</div>' + '<div class="line_div">' + '<p>' + '<img style="width: 18px; height: 18px" class="Emoji" src="http://127.0.0.1:8000/static/face/' + data.id + '.png" alt="" />' + '</p>' + '</div>'

                } else {
                    $div = '<div class="datetime">' + time + '</div>' + '<div class="line_div">'
                        + '<img src="' + data.image_data + '" class="clickable-img">'
                        + '</div>'

                }
            }
            $(".raigth_body").append($div)
            onclickimg()
            setTimeout(function () {
                var element = document.querySelector('.raigth_body');
                element.scrollTop = element.scrollHeight;
            }, 0);
        }
// 点击 #Icon 时显示 .Popover
        $('#Icon').click(async function (event) {
            $('.EmojiPicker').empty()
            event.stopPropagation();  // 阻止事件冒泡，防止触发 document 的点击事件
            $('.Popover').css('display', 'block');
            const r = await getFace()

            // 确保循环次数不超过表情总数
            var totalEmojis = Object.keys(r).length;
            for (let i = 0; i < totalEmojis; i++) {
                const key = Object.keys(r)[i];  // 获取每一个键
                const emoji = r[key];           // 获取对应的表情名称
                // 计算偏移量
                var offsetY = i * -32;  // 每个表情的偏移量，每次向下移动 32px（根据图片高度）

                var newItem = $('<div class="EmojiPicker-item">')
                    .append($('<a class="EmojiPicker-emoji">')
                        .attr('title', `[${emoji}]`)  // 循环使用表情标题
                        .attr('tabindex', '-1')
                        .css('background-position', '0px ' + offsetY + 'px')
                        .append($('<img class="Image">')
                            .attr('alt', '')
                            .attr('src', 'http://127.0.0.1:8000/static/face/' + key + '.png')  // 循环使用表情图片
                            .on('click', function () {
                                sendface(key)
                            })));

                // 将新生成的 item 插入到 EmojiPicker 容器中
                $('.EmojiPicker').append(newItem);
            }


        });

// 点击文档的其他地方时隐藏 .Popover
        $(document).click(function () {
            $('.Popover').css('display', 'none');
        });

// 防止点击 .Popover 时，关闭它
        $('.Popover').click(function (event) {
            event.stopPropagation();  // 阻止点击 .Popover 时触发 document 的点击事件
        });

        function getFace() {
            return new Promise((resolve, reject) => {
                $.ajax({
                    'url': '/service/face/', 'type': 'GET', success: function (response) {
                        if (response.code == 200) {
                            resolve(response.faces);  // 如果请求成功，返回结果
                        } else {
                            reject("Error: " + response.code);  // 如果请求失败，返回错误
                        }
                    }, error: function () {
                        reject("Network error");
                    }
                });
            });
        }

        function sendface(id) {
            $('.Popover').css('display', 'none');

            let message = {
                "username": 'admin', "id": id, 'type': 'face'
            };
            socket.send(JSON.stringify(message));
        }

        $('#Imag').click(function () {
            var fileInput = document.createElement('input')
            fileInput.type = 'file'
            fileInput.accept = 'image/*';  // 限制文件选择框只接受图片文件
            fileInput.addEventListener('change', function (e) {
                var file = e.target.files[0];  // 获取用户选择的第一个文件

                // 检查文件是否是图片
                if (file && file.type.startsWith('image/')) {

                    let time = createtime()
                    // 使用FileReader 读取图片
                    var reader = new FileReader()
                    reader.onload = function (e) {
                        var imagesrc = e.target.result;
                        var fileName = file.name;  // 获取文件名，包括扩展名
                        var fileNameWithoutExt = fileName.substring(0, fileName.lastIndexOf('.'));  // 去掉扩展名
                        let username = $("#username").val()
                        data = {
                            'username': 'admin',
                            'type': 'image',
                            'image_data': imagesrc,
                            'fileName': fileNameWithoutExt
                        }
                        socket.send(JSON.stringify(data))
                    }
                    reader.readAsDataURL(file)

                }
            })
            // 触发文件选择框的点击事件
            fileInput.click();
        })
    }
)

setInterval(function () {
    var numbers = [];


    $(".user_service a").not(":first").each(function () {

        var number = $(this).attr("href").split("=")[1];
        numbers.push(number);
    });
    $.ajax({
        url: '/admin/service/reading/send/', type: 'GET', data: {
            'numbers': numbers,
        }, success: function (response) {
            $(".user_service a").not(":first").each(function () {
                var number = $(this).attr("href").split("=")[1];
                var count = response.data[number]
                if (count != 0) {
                    var counterDiv = $(this).find(".nav-counter.nav-counter-blue");
                    if (counterDiv.length == 1) counterDiv.text(count); else {
                        $div = '<div class="nav-counter nav-counter-blue">' + count + '</div>'
                        div_count = $(this).find(".sercice_text").append($div);
                    }
                }

            });

        }, error: function (error) {

            console.log(error);
        }
    });
}, 2000); // 2000毫秒等于2秒
function updata_reading(event) {
    var url = event.currentTarget.url;
    var parts = url.split("/");
    var number = parts[parts.length - 2];
    $.ajax({
        url: '/admin/service/reading/', // 替换为你的URL
        type: 'GET', data: {
            'number': number,
        }, success: function (data) {

        }, error: function (error) {

            console.log(error);
        }
    });
}

const createtime = () => {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    var time = hours + ':' + minutes;

    return time
}

function enlargeImage(Imgsrc) {
    var overlay = document.querySelector(".overlay");
    var enlargedImg = document.getElementById("enlargedImg");
    enlargedImg.src = Imgsrc;
    console.log('图片被单击');
    overlay.style.display = "flex";
}

function closeOverlay() {
    var overlay = document.querySelector(".overlay");
    overlay.style.display = "none";
}

function onclickimg() {
    $(".raigth_body").on("click", ".clickable-img", function () {
        var imgSrc = $(this).attr("src");
        enlargeImage(imgSrc)
    })
}
// 清空内容并触发 input 事件
function clearTextarea() {
        const textarea = document.getElementById('txt_input');
    textarea.value = ''; // 清空 textarea 内容
    textarea.dispatchEvent(new Event('input')); // 手动触发 input 事件
    textarea.focus(); // 可选：把焦点放回到 textarea
}