# Generated by Django 2.2.5 on 2021-06-02 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20210602_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='lyrics',
            field=models.FileField(blank=True, default='暂无摘要', upload_to='documentLyric/', verbose_name='公文摘要'),
        ),
    ]
