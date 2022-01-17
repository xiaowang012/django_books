#coding-utf-8
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms.fields import CharField,ChoiceField, FileField, IntegerField
from django.forms.widgets import  PasswordInput


#定义表单
#登录表单
class UserForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    password = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})

#注册表单  
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    password = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    password1 = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    def clean(self):  # 全局钩子 确认两次输入的密码是否一致。
        val = self.cleaned_data.get("password")
        r_val = self.cleaned_data.get("password1")
        if val == r_val:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致!")

#录入书本信息的表单
class BooksForm(forms.Form):
    book_name = CharField(min_length=5,max_length=50,error_messages={"required":"书名不能为空!","min_length":"书名长度不能小于5!","max_length":"书名长度不能大于50!"})
    book_type = ChoiceField (initial=2 ,choices = (('1','Python'),('2','C'),('3','C++'),('4','Java'),('5','Javascript'),('6','Linux')))
    book_introduction = CharField(max_length=100,error_messages= {"required":"书本介绍不能为空!","max_length":"书本介绍长度不能超过100!"})
    issue_year = IntegerField(max_value=9999,min_value=2000,error_messages={"required":"年份不能为空!","min_value":"年份不能小于2000年!","max_value":"年份不能大于9999年!"})
    book_file = FileField(required = True,allow_empty_file = False,error_messages={"missing":"文件不能为空!","empty":"不允许上传空文件!"})

#查询书本的表单
class SearchBookForm(forms.Form):
    book_name = CharField(min_length=3,max_length=100,error_messages={"required":"输入框不能为空!","min_length":"搜索内容长度不能小于3!","max_length":"搜索内容长度不能大于100!"})
     
#导入用户表单
class AddUserForm(forms.Form):
    user_file = FileField(required = True,allow_empty_file = False,error_messages={"missing":"文件不能为空!","empty":"不允许上传空文件!"})
