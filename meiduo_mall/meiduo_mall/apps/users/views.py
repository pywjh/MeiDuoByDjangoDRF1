from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView

# Create your views here.


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer





