# django_BookManagement
学习django的过程中写的一个练手小项目 书籍管理程序，
目前只有批量导入用户，查询书籍，下载书籍等功能，
基于Windows,python3.6.5，数据库采用：mysql,
默认账号密码：admin/admin
运行项目步骤：
1.安装依赖包：pip install -r requirements.txt 
2.迁移数据库：
windows：
$ python manage.py migrate 
$ python manage.py makemigrations app1
$ python manage.py migrate app1
3.执行项目：python manage.py runserver 127.0.0.1:5000
