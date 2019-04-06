from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Area

# Create your views here.
class AreaListView(APIView):
    """查询所有省"""

    def get(self, request):
        # 1.获取指定的查询集
        qs = Area.objects.filter(parent=None)
        # 2.创建序列化器进行序列化
        serializer = ''
        # 3.响应
        return Response(serializer.data)
