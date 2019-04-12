from django.shortcuts import render
from rest_framework.views import APIView
import pickle, base64
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection

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
            """
            hash: {'sku_id_1': 2, 'sku_id_16':1}
            set: {sku_id_1}
            """
            # 创建redis连接对象
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()  # 创建管道
            # 添加 如果添加到sku_id在hash中已经存在,需要做增量
            # redis_conn.hincrby('cart_%d % user.id, sku_id, count)
            # redis_conn.hincrby('cart_%d % user.id, sku_id_5, 3)
            # 如果要添加的sku_id在hash字典中不存在,就是新增,如果已存在,就会自动做增量计数再存储
            pl.hincrby('cart_%d' % user.id, sku_id, count)

            # 把勾选的商品sku_id 存储到set集合中
            if selected:  # 判断当前商品是否勾选,勾选的再向set集合中添加
                pl.sadd('selected_%d' % user.id, sku_id)

            # 执行管道
            pl.execute()
            # 响应
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            """未登录用户操作cookie购物车数据"""
            """
            {
                'sku_id_1': {'count': 1, 'selected': True},
                'sku_id_16': {'count': 1, 'selected': True}
            }
            """
            # 获取cookie购物车数据
            cart_str = request.COOKIES.get('cart')
            if cart_str:  # 说明之前cookie购物车已经有商品
                # 把字条串转换成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 把bytes类型的字符串转换成bytes类型
                cart_bytes = base64.b64decode(cart_str_bytes)
                # 把bytes类型转换成字典
                cart_dict = pickle.loads(cart_bytes)
            else:
                # 如果cookie没还没有购物车数据说明是每一次来添加
                cart_dict = {}

            # 增量计数
            if sku_id in cart_dict:
                # 判断当前要添加的sku_id在字典中是否已存在
                origin_count = cart_dict[sku_id]['count']
                count += origin_count  # 原购买数据 和本次购买数据累加
                # count = count + origin_count

            # 把新的商品添加到cart_dict字典中
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            # 先将字典转换成bytes类型
            cart_bytes = pickle.dumps(cart_dict)
            # 再将bytes类型转换成bytes类型的字符串
            cart_str_bytes = base64.b64encode(cart_bytes)
            # 把bytes类型的字符串转换成字符串
            cart_str = cart_str_bytes.decode()

            # 创建响应对象
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            # 设置cookie
            response.set_cookie('cart', cart_str)

            return response





















    def get(self, request):
        """查询"""
        pass

    def put(self, request):
        """修改"""
        pass

    def delete(self, request):
        """删除"""
        pass
