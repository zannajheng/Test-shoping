$(document).ready(function () {

    var files = [];  // 用于存储用户选择的文件
    var handlers = [];  // 用于存储事件处理函数
// 定义事件处理函数
    var handleClick = function (list_top, img) {
        // 删除对应的.list_img元素
        list_top.parentElement.remove();
        // 删除files数组中的对应文件
        var index = parseInt(img.dataset.index);
        console.log(index + '删除的序号')
        // 从files数组中删除对应的文件
        files.splice(index, 1);

        // 更新剩余图片元素的data-index属性
        var list_imgs = document.querySelectorAll('.list_img');
        list_imgs.forEach(function (list_img, index) {
            list_img.querySelector('img').dataset.index = index;
        });
    };


    $('.textarea_uplade').on('click', function () {
        // 检查非undefined的文件数量

        console.log(files)
        if (files.length >= 5) {
            $('.login_message_ajax').css('display', 'block').text('最多可以上传5张截图！');
            // 重置动画
            $('.login_message_ajax').css('animation', 'none');
            setTimeout(function () {
                $('.login_message_ajax').css('animation', '');
            }, 10);
            return;
        }

        // 动态创建一个文件输入元素
        var fileInput = document.createElement('input');
        fileInput.type = 'file';

        // 监听文件选择事件
        fileInput.addEventListener('change', function () {
            var file = this.files[0];
            var extension = file.name.split('.').pop().toLowerCase();

            // 检查文件类型
            var allowedExtensions = ['jpg', 'jpeg', 'png', 'apng', 'gif', 'bmp'];
            if (!allowedExtensions.includes(extension)) {

                $('.login_message_ajax').css('display', 'block').text('不支持的文件类型！请上传JPG，JPEG，PNG，APNG，GIF或BMP文件');
                // 重置动画
                $('.login_message_ajax').css('animation', 'none');
                setTimeout(function () {
                    $('.login_message_ajax').css('animation', '');
                }, 10);
                return;
            }

            files.push(file)
            var index = files.length - 1;
            // 创建一个用于读取文件的FileReader
            var reader = new FileReader();
            reader.onload = function (e) {
                // 创建一个图片元素
                var img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100%';  // 设置图片宽度
                img.style.height = 'auto';  // 设置图片高度

                // 创建一个新的div元素，并添加到页面上
                img.dataset.index = index;
                var div = document.createElement('div');
                div.className = 'list_img';

                var divTop = document.createElement('div');
                divTop.className = 'list_top';
                divTop.appendChild(img);
                var beedback_layer = document.createElement('div')
                beedback_layer.className = 'beedback_layer'
                divTop.appendChild(beedback_layer)

                var divText = document.createElement('div');
                divText.className = 'list_text';
                divText.textContent = file.name;

                div.appendChild(divTop);
                div.appendChild(divText);

                $(".float_img").append(div);
                // 定义事件处理函数

                var list_tops = document.querySelectorAll('.list_top');
                list_tops.forEach(function (list_top, index) {
                    var beedback_layer = list_top.querySelector('.beedback_layer');
                    list_top.addEventListener('mouseenter', function () {
                        beedback_layer.style.display = 'block';
                        this.classList.add('show_after');
                    });
                    list_top.addEventListener('mouseleave', function () {
                        beedback_layer.style.display = 'none';
                        this.classList.remove('show_after');
                    });

                  var img = list_top.querySelector('img');
     var handler = handleClick.bind(null, list_top, img);

                  // 移除旧的监听器
                  if (handlers[index]) {
                      beedback_layer.removeEventListener('click', handlers[index]);
                  }
                  // 添加新的监听器
                  beedback_layer.addEventListener('click', handler);
                  // 更新handlers数组
                  handlers[index] = handler;

                });
            };

            reader.readAsDataURL(file);
        });


        // 触发文件输入元素的点击事件
        fileInput.click();
    });

    $('#button_name').on('click', function () {
        var formData = new FormData();
        files.forEach(function (file, index) {
            formData.append('file' + index, file);
        });

        // 获取文本框和输入框的值
        var textarea_name = $("#textarea_name").val();
        var input_name = $('#input_name').val();
        if (textarea_name.length <= 5) {
            $('.login_message_ajax').css('display', 'block').text('请输入超过5个字符的反馈');
            // 重置动画
            $('.login_message_ajax').css('animation', 'none');
            setTimeout(function () {
                $('.login_message_ajax').css('animation', '');
            }, 10);
            return;
        }

        // 验证input_name是否为手机号码
        var phoneReg = /^1[3-9]\d{9}$/;
        if (!phoneReg.test(input_name)) {

            $('.login_message_ajax').css('display', 'block').text('请输入有效的手机号码');
            // 重置动画
            $('.login_message_ajax').css('animation', 'none');
            setTimeout(function () {
                $('.login_message_ajax').css('animation', '');
            }, 10);
            return;
        }

        // 将这些值添加到formData中
        formData.append('textarea_name', textarea_name);
        formData.append('input_name', input_name);

        $.ajax({
            url: '/user/feedback/upload/',  // 你的上传接口
            type: 'POST',
            data: formData,
            processData: false,  // 告诉jQuery不要处理发送的数据
            contentType: false,  // 告诉jQuery不要设置Content-Type请求头
            success: function (response) {
                console.log(files)
                if (response.code == 200) {
                    $('.login_message_ajax').css('display', 'block').text('反馈成功，正在加紧处理中');
                    $('.login_message_ajax').css('animation', 'none');
                    setTimeout(function () {
                        $('.login_message_ajax').css('animation', '');
                    }, 10);
                    $('.login_message_ajax').on('animationend', function () {
                        window.location.href = '/user/index/';
                    });
                }
            },
            error: function (e) {
                console.log(e)
                console.log('文件上传失败');
            }
        });
    });


})

