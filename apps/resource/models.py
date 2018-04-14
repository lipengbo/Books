from django.db import models

# Create your models here.


class YearBookDes(models.Model):
    year = models.CharField(primary_key=True, max_length=4, db_column='年鉴年份', verbose_name='年鉴年份')
    index = models.CharField(max_length=20, db_column='编号', verbose_name='编号')
    chinese = models.CharField(max_length=40, db_column='年鉴中文名', verbose_name='年鉴中文名')
    english = models.CharField(max_length=60, db_column='年鉴英文名', verbose_name='年鉴英文名')
    author = models.CharField(max_length=20, db_column='责任说明', verbose_name='责任说明')
    unit = models.CharField(max_length=60, db_column='主编单位', verbose_name='主编单位')
    pubtime = models.CharField(max_length=20, db_column='出版日期', verbose_name='出版日期')
    page = models.CharField(max_length=20, db_column='页数', verbose_name='页数')
    money = models.CharField(max_length=20, db_column='人民币定价', verbose_name='人民币定价')
    desc = models.TextField(db_column='内容简介', verbose_name='内容简介')
    image = models.ImageField(upload_to="yearbooks/images/", db_column='封面', verbose_name='封面')

    class Meta:
        db_table = '农业统计年鉴概述'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.year


class YearBookContent(models.Model):
    year = models.ForeignKey(YearBookDes, db_column='年鉴年份', verbose_name='年鉴年份', on_delete=models.DO_NOTHING)
    index = models.IntegerField(db_column='顺序', verbose_name='顺序')
    content = models.CharField(max_length=40, db_column='目录', verbose_name='目录')

    class Meta:
        db_table = '农业统计年鉴目录'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.year_id


class YearBook(models.Model):
    id = models.IntegerField(db_column='id', verbose_name='id', blank=True, null=True)
    title = models.CharField(max_length=60, db_column='标题', verbose_name='标题')
    category = models.CharField(max_length=60, db_column='目录', verbose_name='目录')
    page = models.CharField(max_length=20, db_column='年鉴页码', verbose_name='年鉴页码')
    identify = models.CharField(primary_key=True, max_length=20, db_column='编号', verbose_name='编号')
    year = models.ForeignKey(YearBookDes, db_column='年鉴年份', verbose_name='年鉴年份', on_delete=models.DO_NOTHING)
    caj = models.FilePathField(db_column='CAJ', verbose_name='CAJ', blank=True, null=True)
    pdf = models.FilePathField(db_column='PDF', verbose_name='PDF', blank=True, null=True)
    excel = models.FilePathField(db_column='EXCEL', verbose_name='EXCEL', blank=True, null=True)

    class Meta:
        db_table = '农业统计年鉴详情'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title