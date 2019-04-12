from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class CartView(APIView):
    """购物车增删改查"""

    def post(self, request):
        """新增"""
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
