from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField, TimeField

# Create your models here.
#books表
class Books(models.Model):
    book_name = CharField(max_length=50)
    book_type = CharField(max_length=50)
    book_introduction = TextField()
    issue_year = IntegerField()
    book_file_name = CharField(max_length=100)
    add_book_time = CharField(max_length=100)

# #用户视图的权限表
class Permission(models.Model):
    class Meta:
        permissions = (
            ('views_addbook', '录入书本'),
            ('views_searchbook', '查找书本'),
            ('views_downloadbook', '下载书本'),
            ('views_addusers', '批量导入用户'),
            ('views_downloadexcel', '下载批量导入用户excel模板'),
        )
