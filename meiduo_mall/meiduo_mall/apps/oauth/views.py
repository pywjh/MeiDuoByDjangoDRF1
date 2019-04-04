from django.shortcuts import render
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

# Create your views here.
class QQOauthURLView(APIView):
    """拼接好QQ登录网址"""

    def get(self, request):
        # 1.提取前端传入的next参数记录用户从那里去到login界面
        # next = request.query_params.get('next') or '/'
        # get(self, key, default=None):  获取指定key的值,如果获取的key不存在 可以返回default参数的值
        next = request.query_params.get('next', '/')
        # # QQ登录参数
        # QQ_CLIENT_ID = '101514053'
        # QQ_CLIENT_SECRET = '1075e75648566262ea35afa688073012'
        # QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

        # 2.利用QQ登录SDK
        # oauth = OAuthQQ(client_id=appid, client_secret=appkey, redirect_uri=回调域名, state=记录来源)
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        #  创建QQ登录工具对象
        login_url = oauth.get_qq_url()
        #  调用它里面的方法 拼接好QQ登录网址
        return Response({'login_url': login_url})


class QQAuthUserView(APIView):
    """QQ登录成功后的回调处理"""

    def get(self, request):
        # 获取前端传入的code
        code = request.query_params.get('code')
        if not code: # 如果没有获取到code
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建QQ登录工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        # 调用它里面get_access_token(code) 用code向qq服务器获取access_token
        access_token = oauth.get_access_token(code)
        # 调用它里面的get_open_id(access_token)  用access_token响应QQ服务器获取openid
        openid = oauth.get_open_id(access_token)
        # 查询数据库有没有这个openid
        # 如果没有这个openid 应该创建一个新用户和此openid绑定
        # 如果数据库中有此openid 直接代码登录成功,给前端 返回JWT 状态保存信息
        pass