from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class MyUser(AbstractUser):
    is_secert = models.BooleanField('是否为涉密人员', default=False)
    email = models.CharField('邮箱地址', max_length=50, validators=[EmailValidator('请输入合法的邮箱地址')], )

    def __str__(self):
        return self.username
