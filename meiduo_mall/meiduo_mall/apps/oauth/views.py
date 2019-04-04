from django.shortcuts import render
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from rest_framework.response import Response

# Create your views here.
class QQOauthURLView(APIView):
    """拼接好QQ登录网址"""

    def get(self, request):
        # 1.提取前端传入的next参数记录用户从那里去到login界面
        next = request.query_params.get('next') or '/'


        # 2.利用QQ登录SDK
        oauth = OAuthQQ()
        #  创建QQ登录工具对象
        login_url = oauth.get_qq_url()
        #  调用它里面的方法 拼接好QQ登录网址
        return Response({'login_url': login_url})