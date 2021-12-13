from django.db import models
from django.db.models.base import Model

# Create your models here.
# #用户视图的权限表
class Permission(models.Model):
    class Meta:
        permissions = (
            ('views_host', '访问网页'),
            ('views_addbook', '录入书本'),
            ('views_searchbook', '查找书本'),
            ('views_downloadbook', '下载书本'),
            ('views_addusers', '批量导入用户'),
            ('views_downloadexcel', '下载批量导入用户excel模板'),
        )
