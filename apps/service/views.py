
import random


from django.http import JsonResponse
import string
import time
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages  # 必须正确导入
from django.shortcuts import redirect, render

from apps.service.models import Face
from apps.user.models import Service, Message, Order


# Create your views here.
def service(request):
    number = request.GET.get('number')
    username = request.user.username
    service = Service.objects.get(number=number)
    messages = Message.objects.filter(user=service).order_by('created_at')
    return render(request, 'service.html', {'number': number, 'username': username, 'messages': messages})


def admin_order_update_status(request):
    order_number = request.GET.get('order_number')
    target_state = request.GET.get('status')
    list_url = '/admin/user/order/'

    # 2. 参数验证
    if not order_number or not target_state:
        messages.error(request, '订单号和目标状态不能为空')
        return redirect(list_url)

    try:
        # 3. 查询订单
        orders = Order.objects.filter(order_number=order_number)
        if not orders.exists():
            messages.error(request, f'订单号 {order_number} 不存在')
            return redirect(list_url)

        # 4. 更新状态
        order_count = orders.count()
        orders.update(status=target_state)

        # 5. 显示成功提示
        messages.success(request, f'共 {order_count} 条订单状态已更新为 {target_state}')
        return redirect(list_url)  # 更新成功后跳回列表页

    except Exception as e:
        # 6. 处理异常
        messages.error(request, f'更新失败：{str(e)}')
        return redirect(list_url)


def admin_sercice(request):
    users = User.objects.filter(is_superuser=0)
    for user in users:
        service_number = Service.objects.filter(user=user).exists()
        if not service_number:
            number = random.choice(string.ascii_uppercase) + str(round(time.time() * 1000))
            service = Service(user=user, number=number)
            service.save()
    number = request.GET.get('number')
    user_numbers = ''
    if not number:
        admin_users = User.objects.filter(is_superuser=1)
        user_numbers = Service.objects.exclude(user_id__in=admin_users.values('id'))
    else:
        number_obj = Service.objects.filter(number=number)
        reading = Message.objects.filter(user__in=number_obj).update(reading=1)
        other_services = Service.objects.filter(~Q(number=number), user_id__in=users)
        user_numbers = list(number_obj) + list(other_services)
    messages = Message.objects.filter(user=user_numbers[0]).order_by('created_at')
    for index, i in enumerate(user_numbers):
        if index == 0:
            service = Service.objects.get(number=i.number)
            Message.objects.filter(user=service).update(reading=1)

            # Message.objects.filter(user__in=i).update(reading=1)
            i.count = 0
        else:
            count = Message.objects.filter(reading=0, user=i).count()
            i.count = count
    for item in messages:
        print(item.service)
    return render(request, 'admin_service.html', {'user_numbers': user_numbers, 'messages': messages})


def admin_message(request):
    pass


def admin_reading(request):
    number = request.GET.get('number')
    service = Service.objects.get(number=number)
    Message.objects.filter(user=service).update(reading=1)
    data = {
        'code': 200,
        'message': '更新成功'
    }
    return JsonResponse(data)


def admin_reading_send(request):
    numbers = request.GET.getlist('numbers[]')
    data = {}
    for number in numbers:
        service = Service.objects.get(number=number)
        data[number] = Message.objects.filter(user=service, reading=0).count()

    response = {
        'code': 200,
        'data': data,
        'message': '更新成功'
    }
    return JsonResponse(response)


# 表情包
def face(request):
    if request.method == 'GET':
        faces = Face.objects.all()
        data = {}
        for item in faces:
            key = item.image.replace('.png', '')
            data[key] = item.name
        response = {
            'code': 200,
            'faces': data,
            'message': '操作成功'
        }
        return JsonResponse(response)
