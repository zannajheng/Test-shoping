from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from .models import Goods, Cart, GoodsType, Order, Browse, Evaluate, FeedBack_user, FeedBack_Image

# Register your models here.
admin.site.site_header = '首饰购物商城后台管理'
admin.site.site_title = '购物商城'


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'goods_name', 'intro', 'sell', 'price', 'cation', 'display_image', 'type_id')
    ordering = ('id',)

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.images.url)

    display_image.short_description = '图片'


admin.site.register(Goods, GoodsAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goods_name', 'image', 'count', 'updated_at', 'created_at')
    ordering = ('user', 'updated_at')

    def goods_name(self, obj):
        return Goods.objects.get(id=obj.sku_id).goods_name

    goods_name.short_description = '商品名称'

    def image(self, obj):
        image = Goods.objects.get(id=obj.sku_id).images
        return format_html('<img src="{}" width="50" height="50" />', static(image))

    image.short_description = '图片'


admin.site.register(Cart, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'order_number', 'sku_id', 'count',
        'updated_at', 'created_at', 'status', 'addr', 'tel',
        'operation'  # 确保已添加操作列
    )

    def operation(self, obj):
        app_name = "user"  #
        model_name = "order"

        # 查看的URL
        view_url = f'/admin/{app_name}/{model_name}/{obj.id}/change/'
        if obj.status == '已下单':
            audit_url = f"/admin/order/update?order_number={obj.order_number}&status=已发货"  # 确认发货的URL
            # 使用mark_safe包裹HTML内容
            return mark_safe(f"""
            <a href="{audit_url}" class="btn btn-success btn-sm">确认发货</a>
            <a href="{view_url}" class="btn btn-primary btn-sm">查看</a>
            """)
        else:
            return mark_safe(f"""
            <a href="{view_url}" class="btn btn-primary btn-sm">查看</a>
            """)

    # 移除allow_tags，改用mark_safe
    operation.short_description = '操作'  # 列标题


admin.site.register(Order, OrderAdmin)


class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'goods_type_name', 'display_image', 'class_name')
    ordering = ('id',)

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="70" />', obj.images.url)

    display_image.short_description = '图片'


admin.site.register(GoodsType, GoodsTypeAdmin)


class BrowseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sku_id', 'image', 'updated_at', 'created_at')
    ordering = ('user',)

    def image(self, obj):
        image = obj.sku_id.images
        return format_html('<img src="{}" width="50" height="50" />', image.url)

    image.short_description = '图片'


admin.site.register(Browse, BrowseAdmin)


class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku_id', 'evaluate', 'updated_at', 'created_at')
    ordering = ('id',)


admin.site.register(Evaluate, EvaluateAdmin)


class Feedback_UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'textarea_name', 'input_name', 'feedback_number', 'display_images', 'created_at')
    ordering = ('-created_at',)

    def display_images(self, obj):
        images = FeedBack_Image.objects.filter(feedback_number=obj)
        return format_html_join('\n', '<img src="{}" width="50" height="50" />',
                                ((image.file.url,) for image in images))

    display_images.short_description = '图片'


admin.site.register(FeedBack_user, Feedback_UserAdmin)
