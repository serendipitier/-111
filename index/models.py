from django.db import models

# Create your models here.


# 公文分类表
class Label(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('分类标签', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '公文分类'
        verbose_name_plural = '公文分类'


# 公文信息表
class Document(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('公文标题', max_length=50)
    office = models.CharField('发文机关', max_length=50)
    person = models.CharField('上传者', max_length=20)
    type = models.CharField('公文类型', max_length=20, default='')
    key = models.BinaryField('公文密钥', max_length=200, default=b'')
    Classification = models.BooleanField('是否涉密', default=False)
    time = models.DateField('上传时间')
    img = models.FileField('公文缩略图', upload_to='documentImg/')
    lyrics = models.FileField('公文摘要', upload_to='documentLyric/', default='暂无摘要', blank=True)
    file = models.FileField('公文文件', upload_to='documentFile/')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='公文分类')

    def __str__(self):
        return self.name

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '公文信息'
        verbose_name_plural = '公文信息'


# 公文动态表
class Dynamic(models.Model):
    id = models.AutoField('序号', primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='公文标题')
    plays = models.IntegerField('查看次数', default=0)
    search = models.IntegerField('搜索次数', default=0)
    download = models.IntegerField('下载次数', default=0)

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '公文动态'
        verbose_name_plural = '公文动态'


# 公文批复表
class Comment(models.Model):
    id = models.AutoField('序号', primary_key=True)
    text = models.CharField('内容', max_length=500)
    user = models.CharField('用户', max_length=20)
    date = models.DateField('日期', auto_now=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='公文名')

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '公文批复'
        verbose_name_plural = '公文批复'