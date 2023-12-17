# Generated by Django 2.2.5 on 2021-06-05 09:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.CharField(max_length=50, validators=[django.core.validators.EmailValidator('请输入合法的邮箱地址')], verbose_name='邮箱地址'),
        ),
    ]
