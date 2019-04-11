from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import SKU
from .serializers import SKUSerializer


# Create your views here.
class SKUListView(ListAPIView):
    """商品列表数据查询"""

    serializer_class = SKUSerializer
    # queryset = SKU.objects.filter()

    def get_queryset(self):
        """如果当前在视图中没有去定义get /post方法 那么就没法定义一个参数用来接收正则组提取出来的url路径参数, 可以利用视图对象的 args或kwargs属性去获取啊"""
        category_id = self.kwargs.get('category_id')
        return SKU.objects.filter(is_launched=True, category_id=category_id)
