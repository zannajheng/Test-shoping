import base64
import json
import os
import uuid

from apps.user.models import Message, Service
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from shoping import settings


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print('发起连接。。。。')
        self.accept()
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        mes = ''
        group = self.scope['url_route']['kwargs'].get('group')
        data = json.loads(message['text'])
        service = Service.objects.get(number=group)
        if data['type'] == 'text':
            if data['username'] == 'admin':
                mes = Message(user=service, status = 1, service = data['text'])
            else:
                mes = Message(user=service, status=0, service=data['text'])
        elif data['type'] == 'face':
            if data['username'] == 'admin':
                mes = Message(user=service, status=1, service=data['id'], type='face')
            else:
                mes = Message(user=service, status=0, service=data['id'], type='face')
        else:
            imageName = self.save_image(data['image_data'], data['fileName'])
            if data['username'] == 'admin':
                mes = Message(user=service, status=1, service=imageName, type='image')
            else:
                mes = Message(user=service, status=0, service=imageName, type='image')
        mes.save()
        async_to_sync(self.channel_layer.group_send)(group, {"type": "group_send", "message": message})

    def group_send(self, message):
        text = message['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()

    def save_image(self, image_data, fileName):
        """
        解码图像数据并保存为文件
        """
        # 从 base64 编码的图像中提取文件内容
        format, imgstr = image_data.split(';base64,')  # 获取 base64 字符串
        print('format:', format)
        ext = format.split('/')[1]  # 获取图片格式，比如 'jpeg', 'png'
        image_data_decoded = base64.b64decode(imgstr)  # 解码 base64 数据

        # 生成文件名
        image_name = f"{fileName}.{ext}"
        image_path = os.path.join(settings.MEDIA_ROOT, 'service', image_name)
        if os.path.exists(image_path):
            image_name = f"{uuid.uuid4()}.{ext}"
            image_path = os.path.join(settings.MEDIA_ROOT, 'service', image_name)
        # 保存图像到服务器文件系统
        os.makedirs(os.path.dirname(image_path), exist_ok=True)  # 创建目录
        with open(image_path, 'wb') as f:
            f.write(image_data_decoded)
        return image_name