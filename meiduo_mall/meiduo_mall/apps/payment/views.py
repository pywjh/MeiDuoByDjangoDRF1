from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class PaymentView(APIView):
    """生成支付链接"""

    def get(self, request, order_id):

        # 校验订单的有效性

        # 创建alipay  SDK中提供的支付对象

        # 调用SDK的方法得到支付链接后面的查询参数

        # 拼接好支付链接

        # 响应
        pass