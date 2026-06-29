from django.contrib import messages
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse

class AuthLogin(MiddlewareMixin):
    def process_request(self, request):
        noauth_url_list = [
            '/user/login/', '/user/register/', '/user/password/', '/user/index/', '/user/detail/',
            '/user/search/', '/admin/login/', '/media/', '/user/login/', '/user/logout/', '/user/verify/code/'
        ]
        url_is_exempt = any(url in request.path_info for url in noauth_url_list) or request.path_info.startswith('/admin/')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if (url_is_exempt and not is_ajax) or is_ajax:
            return

        try:
            match = resolve(request.path_info)
            if match.url_name == 'detail':
                return
        except:
            pass
        info = request.session.get('info')
        if info:
            return
        messages.error(request, '请先登录，然后再进行操作。')
        if request.path_info == '/user/cartadd/':
            data = {
                'code': 302,
                'messsage': '用户未登录'
            }
            return JsonResponse(data)

        return redirect('login')