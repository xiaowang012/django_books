# Generated by Django 3.2.9 on 2021-12-13 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_books_add_book_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('views_host', '访问网页'), ('views_login', '登录网页'), ('views_register', '用户注册'), ('views_management', '后台管理'), ('views_logout', '用户登出'), ('views_addbook', '录入书本'), ('views_searchbook', '查找书本'), ('views_downloadbook', '下载书本'), ('views_addusers', '批量导入用户'), ('views_downloadexcel', '下载批量导入用户excel模板')),
            },
        ),
    ]
