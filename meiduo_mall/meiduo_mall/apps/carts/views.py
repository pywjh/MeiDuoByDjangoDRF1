from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import CartSerializer


# Create your views here.
class CartView(APIView):
    """购物车增删改查"""

    def perform_authentication(self, request):
        """重写此方法 直接pass 可以延后认证 延后到第一次通过 request.user 或request.auth才去做认证"""
        pass

    def post(self, request):
        """新增"""
        # 创建序列化器进行反序列化
        serializer = CartSerializer(data=request.data)
        # 调用is_valid进行校验
        serializer.is_valid(raise_exception=True)
        # 获取校验后的数据
        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get('count')
        selected = serializer.validated_data.get('selected')


        try:
            user = request.user  # 执行次行代码时会执行认证逻辑,如果登录用户认证会成功没有异常,但是未登录用户认证会出异常我们自己拦截
        except:
            user = None
        # is_authenticated 判断是匿名用户还是 登录用户  (判断用户是否通过认证)
        if user and user.is_authenticated:
            """登录用户操作redis购物车数据"""

        else:
            """未登录用户操作cookie购物车数据"""
        pass

    def get(self, request):
        """查询"""
        pass

    def put(self, request):
        """修改"""
        pass

    def delete(self, request):
        """删除"""
        pass
