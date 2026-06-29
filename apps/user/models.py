from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password, check_password


class GoodsType(models.Model):
    goods_type_name = models.CharField(max_length=255, verbose_name='商品类型名称')
   # images = models.CharField(max_length=255, verbose_name='类型图片路径')
    images = models.ImageField(
        upload_to='images/',
        verbose_name="分类图片",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
    class_name = models.CharField(max_length=255, verbose_name='标签')

    class Meta:
        db_table = 'goods_type'
        verbose_name = '商品类型'

    def __str__(self):
        return self.goods_type_name


class Goods(models.Model):
    goods_name = models.CharField(max_length=255, verbose_name = '首饰名称')
    intro = models.CharField(max_length=255, verbose_name='首饰说明')
    sell = models.IntegerField(verbose_name='售出')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    cation = models.CharField(max_length=255, verbose_name='单位')
    #images = models.CharField(max_length=255, verbose_name='图片路径')
    images = models.ImageField(
        upload_to='images/',
        verbose_name="首饰图片",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
    type_id = models.ForeignKey(GoodsType, on_delete=models.CASCADE, verbose_name='首饰所属类型')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品信息'
    def __str__(self):
        return self.goods_name

class Cart(models.Model):
    user = models.CharField(max_length=255, verbose_name='用户')
    sku_id = models.IntegerField(verbose_name='商品ID')
    count = models.IntegerField(verbose_name='数量')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'cart'
        verbose_name  = '购物车信息'



class Order(models.Model):
    user = models.CharField(max_length=255, verbose_name='用户')
    order_number = models.CharField(max_length=255, verbose_name='订单号')
    count = models.IntegerField(verbose_name='商品数量')
    status = models.CharField(max_length=20, verbose_name='订单状态')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    sku_id = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    evaluate = models.IntegerField(choices=((0, '未评价'), (1, '已评价')), default=0, verbose_name='是否评价')
    addr = models.CharField(max_length=250, verbose_name='收货地址')
    tel = models.CharField(max_length=20, verbose_name='联系电话')
    class Meta:
        db_table = 'order'

class Browse(models.Model):
    user = models.CharField(max_length=255, verbose_name='用户')
    sku_id = models.ForeignKey(Goods, on_delete=models.CASCADE, db_column='sku_id', verbose_name='商品')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'browse'

class Evaluate(models.Model):
    user = models.CharField(max_length=255)
    sku_id = models.ForeignKey(Goods, on_delete=models.CASCADE, db_column='sku_id', verbose_name='商品')
    evaluate = models.CharField(max_length=1000, verbose_name='商品评论')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = 'evaluate'
        verbose_name  = '商品评论'

class FeedBack_user(models.Model):
    user = models.CharField(max_length=255, verbose_name='用户')
    textarea_name = models.TextField(verbose_name='反馈内容')
    input_name = models.CharField(max_length=255, verbose_name='手机号码')
    feedback_number = models.CharField(max_length=255, unique=True, verbose_name='反馈ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='反馈时间')

    class Meta:
        db_table = 'feedback_user'
        verbose_name = '用户反馈'

class FeedBack_Image(models.Model):
    feedback_number = models.ForeignKey(FeedBack_user, on_delete=models.CASCADE, to_field='feedback_number', verbose_name='反馈ID')
    file = models.FileField(upload_to='uploads/')

    class Meta:
        db_table = 'feedback_image'

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=255)

    class Meta:
        db_table = 'service'

class Message(models.Model):
    STAUSE = [(0, '发送'), (1, '接收')]
    user = models.ForeignKey(Service, on_delete=models.CASCADE,)
    status = models.IntegerField(choices=STAUSE)
    service = models.CharField(max_length=255, default='hello')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    READING = [(0, '未读'), (1, '已读')]
    reading = models.IntegerField(choices=READING, default=0)
    type = models.CharField(max_length=255, verbose_name='消息类型', default='text')
    class Meta:
        db_table = 'message'




