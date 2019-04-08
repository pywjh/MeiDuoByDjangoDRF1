from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin

from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, UserAddressSerializer, AddressTitleSerializer
from .models import User, Address


# Create your views here.


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """判断用户是否已注册"""

    def get(self, request, username):
        # 查询user表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'username': username,
            'count': count
        }
        # 响应
        return Response(data)


class MobileCountView(APIView):
    """判断手机号是否已注册"""

    def get(self, request, mobile):
        # 查询数据库
        count = User.objects.filter(mobile=mobile).count()
        # 构造响应数据
        data = {
            'mobile': mobile,
            'count': count
        }
        # 响应
        return Response(data)


# GET /user/
class UserDetailView(RetrieveAPIView):
    """用户详细信息展示"""
    serializer_class = UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 指定权限,只有通过认证的用户才能访问当前视图

    def get_object(self):
        """重写此方法返回 要展示的用户模型对象"""
        return self.request.user


# PUT /email/
class EmailView(UpdateAPIView):
    """更新用户邮箱"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


class EmailVerifyView(APIView):
    """激活用户邮箱"""

    def get(self, request):
        # 获取前端查询字符串中传入的token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 把token解密 并查询对应的user
        user = User.check_verify_email_token(token)
        # 修改当前user的email_active为True
        if user is None:
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        # 响应
        return Response({'message': 'ok'})


class AddressViewSet(UpdateModelMixin, GenericViewSet):
    """用户收货地址增删改查"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

    # queryset = ''
    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)
        # return Address.objects.filter(is_deleted=False)

    def create(self, request):
        user = request.user
        # count = user.addresses.all().count()
        count = Address.objects.filter(user=user).count()
        # 用户收货地址数量有上限  最多只能有20
        if count >= 20:
            return Response({'message': '收货地址数量上限'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建序列化器进行反序列化
        serializer = self.get_serializer(data=request.data)
        # 调用序列化器的is_valid()
        serializer.is_valid(raise_exception=True)
        # 调用序列化器的save()
        serializer.save()
        # 响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 20,
            'addresses': serializer.data,
        })

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

        # put /addresses/pk/title/
        # 需要请求体参数 title

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)