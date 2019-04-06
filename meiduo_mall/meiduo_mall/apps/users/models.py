from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱激活状态')

    class Meta:  # 配置数据库表名,及设置模型在admin站点显示的中文名
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_email_verify_url(self):
        """生成邮箱激活链接"""
        # 1.创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)

        # 2.调用dumps方法进行加密, bytes
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()

        # 3.拼接激活url
        return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token