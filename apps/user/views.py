import json
import math

from PIL import Image, ImageDraw, ImageFont
from six import BytesIO
import os
from django.views.decorators.csrf import csrf_exempt
from .utils.pay import AliPay
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.templatetags.static import static
from django.utils import timezone
import string
import time
from django.db.models import Subquery, OuterRef
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import GoodsType, Goods, Cart, Order, Browse, Evaluate, FeedBack_user, FeedBack_Image, Service, Message
from itertools import groupby
import random
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from apps.user.utils.form import RegisterForm, Login
from django.contrib.auth import authenticate, login, logout


def index(request):
    goods_type_names = GoodsType.objects.all()
    goods_list = Goods.objects.all().order_by('type_id_id')
    goods = {k: list(v) for k, v in groupby(goods_list, key=lambda x: x.type_id_id)}
    data_list = [
        {
            'goods_type': gt,
            'goods': goods.get(gt.id, [])
        }
        for gt in goods_type_names
    ]
    return render(request, 'index.html', {'data_list': data_list, })


def detail(request, sku_id):
    goods = Goods.objects.get(id=sku_id)
    brwose, created = Browse.objects.get_or_create(
        user=request.user,
        sku_id=goods,
        defaults={'updated_at': timezone.now()}
    )
    brwoses = Browse.objects.filter(user=request.user)
    if brwoses.count() > 10:
        brwose = brwoses.order_by('updated_at').first()
        brwose.delete()
    if not created:
        brwose.updated_at = timezone.now()
        brwose.save()
    goods_all = Goods.objects.all()
    goods = Goods.objects.filter(id=sku_id).first()
    rands = goods_all[random.randint(0, len(goods_all) - 1)]
    evaluates = Evaluate.objects.filter(sku_id=sku_id)

    return render(request, 'detail.html', {'goods': goods, 'rands': rands, 'evaluates': evaluates})


def user_login(request):
    if request.method == 'GET':
        if request.GET.get('is_login'):
            messages.error(request, '请先登录，然后再进行操作。')
        loginform = Login()
    else:
        loginform = Login(request.POST, request=request)
        if loginform.is_valid():
            user_name = loginform.cleaned_data['user']
            password = loginform.cleaned_data['password']
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                user_obj = User.objects.get(username=user_name)
                request.session['info'] = {'id': user_obj.id, 'username': user_obj.username}
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('index')
            else:
                messages.error(request, "密码不正确！")
        else:
            for field, errors in loginform.errors.items():
                user_input = loginform.cleaned_data.get('user')
                for error in errors:
                    if error == '用户不存在':
                        messages.error(request, f"{user_input}: {error}")
                    if error == '密码长度在5-20之间':
                        messages.error(request, f"用户{error}")
                    # if error == '验证码错误':
                    #     messages.error(request, f"验证码错误")
            user = request.POST.get('user')
            loginform = Login(initial={'user': user}, request=request)
    return render(request, 'login.html', {'form': loginform})


def login_check(request):
    uname = request.GET.get('uname')
    user = User.objects.filter(username=uname).exists()
    if user:
        data = {
            'code': 200,
            'count': 1
        }
        return JsonResponse(data)
    data = {
        'code': 200,
        'count': 0
    }
    return JsonResponse(data)


def register(request):
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
def register_submit(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data['user']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        password_confirmation = form.cleaned_data['password_confirmation']
        username = User.objects.filter(username=user).exists()
        if (username):
            data = {
                'code': 302,
                'message': '用户已存在'
            }
            return JsonResponse(data)
        if (password != password_confirmation):
            data = {
                'code': 302,
                'message': '两次密码不一致'
            }
            return JsonResponse(data)
        user = User.objects.create_user(
            username=user,
            email=email,
            password=password
        )
        user.save()
        data = {
            'code': 200,
            'message': '注册成功'
        }
        return JsonResponse(data)
    data = {
        'code': 302,
        'message': '验证失败'
    }
    return JsonResponse(data)


def register_check(request):
    uname = request.GET.get('uname', None)
    user = User.objects.filter(username=uname).exists()
    if not user:
        data = {
            'code': 200,
            'count': 0,
        }
        return JsonResponse(data)
    data = {
        'code': 200,
        'count': 1,
    }
    return JsonResponse(data)


def user_logout(request):
    request.session.clear()
    logout(request)
    return redirect('login')


def password(request):
    if request.method == 'GET':
        return render(request, 'password.html')
    user = request.POST.get('user')
    password = request.POST.get('password')
    password_confirmation = request.POST.get('password_confirmation')
    if len(password) < 6:
        messages.error(request, '密码最少为6个字符')
        return redirect('password')
    if password_confirmation != password:
        messages.error(request, '两次密码不一致')
    user_exists = User.objects.filter(username=user).exists()
    if not user_exists:
        messages.error(request, '用户不存在')
        return redirect('password')
    try:
        user = User.objects.get(username=user)
        user.set_password(password)
        user.save()
        return redirect('login')
    except:
        messages.error(request, '操作出错，重试')
    return redirect('password')


def cartadd(request):
    if not request.user.is_authenticated:
        data = {
            'code': 302,
            'message': '用户未登录'
        }
        return JsonResponse(data)

    user = request.user
    sku_id = request.POST.get('sku_id')
    num = request.POST.get('num_show')
    num = int(num)
    cart, created = Cart.objects.get_or_create(
        user=user,
        sku_id=sku_id,
        defaults={'count': num}
    )
    if not created:
        cart.count += num
        cart.save()
    count = Cart.objects.filter(user=request.user).count()
    data = {
        'code': 200,
        'count': count,
        'message': '加入购物车成功'
    }
    return JsonResponse(data)


def cart_count(request):
    if request.user.is_authenticated:
        num = Cart.objects.filter(user=request.user).count()
    else:
        num = 0
    number = None
    try:
        user = User.objects.get(username=request.user.username)
        service, created = Service.objects.get_or_create(user=user)
        if created:
            service.number = random.choice(string.ascii_uppercase) + str(round(time.time() * 1000))
            service.save()
        number = Service.objects.get(user=user)
    except:
        print("没登录--")
    return {'cart_count': num, 'number': number}


def cart(request):
    if request.method == 'GET':
        cart = Cart.objects.filter(user=request.user).order_by('-created_at')
        count = len(cart)
        goods_list = []
        sum = 0
        for i in cart:
            try:
                goods = Goods.objects.get(id=i.sku_id)
            except Goods.DoesNotExist:
                continue
            total_price = goods.price * i.count
            sum += total_price
            goods_list.append((goods, i.count, total_price))
        return render(request, 'cart.html', {'goods_list': goods_list, 'sum': sum, 'count': count})
    data = json.loads(request.body)
    goods = data.get('goods')
    order_number = random.choice(string.ascii_uppercase) + str(round(time.time() * 1000))
    for item in goods:
        sku_id = item['sku_id']
        count = item['count']
        Order.objects.create(
            user=request.user,
            sku_id_id=sku_id,
            count=count,
            order_number=order_number,
            status='已下单',
            addr=item['addr'],
            tel=item['tel'],
        )
        Cart.objects.get(user=request.user, sku_id=sku_id).delete()
    data = {
        'code': 200,
        'message': '订单生成'
    }
    time.sleep(3)
    return JsonResponse(data)


def cart_add(request):
    sku_id = request.POST.get('sku_id')
    cart = Cart.objects.get(user=request.user, sku_id=sku_id)
    cart.count += 1
    cart.save()
    data = {
        'code': 200,
        'message': '添加成功'
    }
    return JsonResponse(data)


def cart_decr(request):
    sku_id = request.POST.get('sku_id')
    cart = Cart.objects.get(user=request.user, sku_id=sku_id)
    cart.count -= 1
    cart.save()
    data = {
        'code': 200,
        'message': '操作成功'
    }
    return JsonResponse(data)


def cart_delete(request):
    sku_id = request.POST.get('sku_id')
    Cart.objects.get(user=request.user, sku_id=sku_id).delete()
    data = {
        'code': 200,
        'message': '删除成功'
    }
    return JsonResponse(data)


def order(request):
    latest_orders = Order.objects.filter(user=request.user, order_number=OuterRef('order_number')).order_by(
        '-created_at')
    numbers = Order.objects.filter(user=request.user, id=Subquery(latest_orders.values('id')[:1])).order_by(
        '-created_at')
    orders = []
    for number in numbers:
        goods = Order.objects.filter(user=request.user, order_number=number.order_number).select_related('sku_id')
        orders.append(goods)
    for item in orders:
        sum = 0
        for i in item:
            count = Order.objects.get(order_number=item[0].order_number, sku_id=i.sku_id.id)
            i.sku_id.count = count.count
            i.sku_id.total = count.count * i.sku_id.price
            sum += count.count * i.sku_id.price
        item[0].sum = sum
    paginator = Paginator(orders, 5)
    page = request.GET.get('page', 1)
    orders = paginator.page(page)
    return render(request, 'order.html', {'orders': orders})


def user_center(request):
    user = request.user
    browses = Browse.objects.filter(user=user).order_by('-updated_at')
    goods_list = [Goods.objects.get(id=browse.sku_id.id) for browse in browses]
    return render(request, 'usercenter.html', {'user': user, 'goods_list': goods_list})


def address(request):
    return render(request, 'address.html')


def search(request):
    query = request.GET.get('query')
    goods_list = Goods.objects.filter(goods_name__icontains=query)
    paginator = Paginator(goods_list, 12)
    page = request.GET.get('page', 1)
    goods = paginator.page(page)
    return render(request, 'search.html', {'query': query, 'goods': goods})


def search_cartadd(request):
    sku_id = request.POST.get('sku_id')
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        sku_id=sku_id,
        defaults={'count': 1}
    )
    if not created:
        cart.count += 1
        cart.save()
    count = Cart.objects.filter(user=request.user).count()
    data = {
        'code': 200,
        'message': '操作成功',
        'count': count
    }
    return JsonResponse(data)


def search_page(request):
    query = request.GET.get('query')
    page = request.GET.get('page')
    goods_list = Goods.objects.filter(goods_name__icontains=query)

    paginator = Paginator(goods_list, 12)
    try:
        goods = paginator.page(page)
    except:
        # 获取商品数量
        count = goods_list.count()

        # 每页显示 12 个商品，向上取整计算页数
        pages = math.ceil(count / 12)
        data = {
            'code': -1,
            'message': '数据为空',
            'pages': pages
        }
        return JsonResponse(data)
    goods_data = list(goods.object_list.values())
    for i in goods_data:
        i['images'] = static(i['images'])
        i['intro'] = reverse('detail', args=[i['id']])
    data = {
        'code': 200,
        'goods_data': goods_data
    }
    return JsonResponse(data)


def payment(request, order_number):
    orders = Order.objects.filter(order_number=order_number)
    goods = []
    payment_sum = 0

    for order in orders:
        total = 0
        good = order.sku_id
        good.count = order.count
        good.total = good.count * good.price
        payment_sum += good.count * good.price
        goods.append(good)
    goods_count = len(goods)
    return render(request, 'payment.html', {'goods': goods, 'payment_sum': payment_sum, 'goods_count': goods_count,
                                            'order_number': order_number})


def more_list(request):
    type_id = request.GET.get('type_id')
    # 其他类型的商品（排除当前type_id），直接在数据库层过滤，避免 while 死循环
    other_goods = list(Goods.objects.exclude(type_id=type_id))
    rand_goods = []
    # 打乱其他商品列表并取前 2 个
    if other_goods:
        random.shuffle(other_goods)
        rand_goods = other_goods[:2]
    goods = Goods.objects.filter(type_id=type_id)
    paginator = Paginator(goods, 10)
    page = request.GET.get('page', 1)
    goods = paginator.page(page)
    return render(request, 'more_list.html', {'goods': goods, 'rand_goods': rand_goods, 'type_id': type_id})


def more_list_price(request):
    type_id = request.GET.get('type_id')
    page = request.GET.get('page', 1)
    goods = Goods.objects.filter(type_id=type_id).order_by('-price')
    paginator = Paginator(goods, 10)
    try:
        goods = paginator.page(page)
    except EmptyPage as e:
        print(e)
        data = {
            'code': 500,
            'message': '数据为空'
        }
        return JsonResponse(data)
    goods = list(goods.object_list.values())
    data = {
        'code': 200,
        'goods': goods
    }
    for good in goods:
        good['images'] = static(good['images'])
        good['intro'] = reverse('detail', args=[good['id']])
    return JsonResponse(data)


def more_list_page(request):
    page = request.GET.get('page')
    type_id = request.GET.get('type_id')
    goods = Goods.objects.filter(type_id=type_id)
    paginator = Paginator(goods, 10)
    page = request.GET.get('page', page)
    try:
        goods = paginator.page(page)
    except EmptyPage as e:
        # 获取商品数量
        count = goods.count()

        # 每页显示 10 个商品，向上取整计算页数
        pages = math.ceil(count / 10)
        data = {
            'code': 500,
            'message': '数据为空',
            'pages': pages
        }
        return JsonResponse(data)
    goods = list(goods.object_list.values())
    for good in goods:
        good['images'] = static(good['images'])
        good['intro'] = reverse('detail', args=[good['id']])
    data = {
        'code': 200,
        'message': '操作成功',
        'goods': goods
    }
    return JsonResponse(data)


def order_update_status(request):
    # 获取订单号和要修改的目标状态
    order_number = request.GET.get('order_number')
    target_state = request.GET.get('status')  # 接收要修改的目标状态

    # 验证参数是否存在
    if not order_number or not target_state:
        messages.error(request, '订单号和目标状态不能为空')
        return redirect('order')  # 跳转到订单列表页或其他合适页面

    try:
        # 查询所有相同订单号的订单
        orders = Order.objects.filter(order_number=order_number)

        # 检查是否存在该订单号的订单
        if not orders.exists():
            messages.error(request, '订单不存在')
            return redirect('order')

        # 获取符合条件的订单数量
        order_count = orders.count()

        # 更新所有相同订单号的订单状态
        orders.update(status=target_state)

        # 根据订单数量返回不同的提示信息
        if order_count == 1:
            messages.success(request, f'订单状态已更新为 {target_state}')
        else:
            messages.success(request, f'共 {order_count} 条相同编号的订单状态已更新为 {target_state}')

        return redirect('order')

    except Exception as e:
        messages.error(request, f'修改失败：{str(e)}')
        return redirect('order')


def order_delete(request):
    order_number = request.GET.get('order_number')

    if not order_number:
        messages.error(request, '订单号不能为空')
        return redirect('order')

    try:
        # 查询所有相同订单号的订单
        orders = Order.objects.filter(order_number=order_number)

        # 检查订单是否存在
        if not orders.exists():
            messages.error(request, '订单不存在')
            return redirect('order')

        # 检查是否有已发货的订单
        shipped_orders = orders.filter(status='已发货')
        if shipped_orders.exists():
            # 统计已发货订单数量
            shipped_count = shipped_orders.count()
            total_count = orders.count()
            if total_count == shipped_count:
                messages.error(request, '所有相同编号的订单均已发货，不能删除')
            else:
                messages.error(request, f'有 {shipped_count} 条相同编号的订单已发货，不能删除')
            return redirect('order')

        # 执行删除操作
        deleted_count, _ = orders.delete()
        messages.success(request, f'成功删除 {deleted_count} 条相同编号的订单')
        return redirect('order')

    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
        return redirect('order')


def order_evaluate(request):
    if request.method == 'GET':
        order_number = request.GET.get('order_number')
        order = Order.objects.filter(order_number=order_number).first()
        orders = Order.objects.filter(order_number=order_number)
        goods = []
        for item in orders:
            good = item.sku_id
            good.count = item.count
            good.total = item.count * item.sku_id.price
            good.evaluate = item.evaluate
            goods.append(good)
        return render(request, 'order_evaluate.html', {'goods': goods, 'order': order})


def order_evaluate_sumbit(request):
    order_number = request.POST.get('order_number')
    reviews = json.loads(request.POST['reviews'])
    page = 0
    for item in reviews:
        if item['evaluate']:
            goods = Goods.objects.get(id=item['sku_id'])
            order = Order.objects.get(sku_id=item['sku_id'], order_number=order_number)
            order.evaluate = 1
            order.save()
            evaluate = Evaluate(evaluate=item['evaluate'], sku_id=goods, user=order.user)
            evaluate.save()
            page += 1
        if page:
            page += 1
    data = {
        'code': 200,
        'page': f'添加{page}条评论！'
    }
    return JsonResponse(data)


def index_detail_buy(request):
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    order_number = random.choice(string.ascii_uppercase) + str(round(time.time() * 1000))
    goods = Goods.objects.get(id=sku_id)
    order = Order(user=request.user, sku_id=goods, count=count, order_number=order_number, status='未支付')
    order.save()
    data = {
        'code': 200,
        'message': '操作成功',
        'order_number': order_number
    }
    return JsonResponse(data)


def feedback(request):
    return render(request, 'feedback.html')


@csrf_exempt
def feedback_upload(request):
    username = request.user.username
    feedback_number = ''.join(random.choices(string.ascii_uppercase, k=2)) + '-' + str(round(time.time() * 1000))
    textarea_name = request.POST.get('textarea_name')
    input_name = request.POST.get('input_name')
    feedback = FeedBack_user(user=username, textarea_name=textarea_name, input_name=input_name,
                             feedback_number=feedback_number)
    feedback.save()
    for i in range(5):
        file_key = 'file' + str(i)
        if file_key in request.FILES:
            file = request.FILES[file_key]
            feedback_img = FeedBack_Image(feedback_number=feedback, file=file)
            feedback_img.save()

    data = {
        'code': 200,
        'message': '反馈成功'
    }
    return JsonResponse(data)


def verify_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (224, 224, 224)
    width = 100
    height = 34
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('arial.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    request.session.set_expiry(60)
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'PNG')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
