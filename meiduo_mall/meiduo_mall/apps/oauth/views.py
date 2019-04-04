from django.shortcuts import render
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from rest_framework.response import Response


# Create your views here.
class QQOauthURLView(APIView):
    """拼接好QQ登录网址"""

    def get(self, request):
        # 1.提取前端传入的next参数记录用户从那里去到login界面
        # next = request.query_params.get('next') or '/'
        # get(self, key, default=None):  获取指定key的值,如果获取的key不存在 可以返回default参数的值
        next = request.query_params.get('next', '/')
        # QQ登录参数
        QQ_CLIENT_ID = '101514053'
        QQ_CLIENT_SECRET = '1075e75648566262ea35afa688073012'
        QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

        # 2.利用QQ登录SDK
        # oauth = OAuthQQ(client_id=appid, client_secret=appkey, redirect_uri=回调域名, state=记录来源)
        oauth = OAuthQQ(client_id=QQ_CLIENT_ID, client_secret=QQ_CLIENT_SECRET, redirect_uri=QQ_REDIRECT_URI,
                        state=next)
        #  创建QQ登录工具对象
        login_url = oauth.get_qq_url()
        #  调用它里面的方法 拼接好QQ登录网址
        return Response({'login_url': login_url})
