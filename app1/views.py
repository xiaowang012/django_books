#coding=utf-8
from django.http.response import HttpResponse,FileResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required,permission_required
#from django.views.decorators.csrf import csrf_exempt, csrf_protect
from . import My_forms
from . import models
import time
import os
import zipfile
import xlrd
from django.contrib.auth.models import Permission as PER
from django.contrib.contenttypes.models import ContentType


def add_permissions(user_id):
    #普通用户只有下载书本和查找书本的权限，登录，注册不做限制
    user = get_object_or_404(User, pk = user_id)
    #清除权限
    user.user_permissions.clear()
    content_type = ContentType.objects.get_for_model(models.Permission)
    #自定义的查询视图的权限
    permission1 = PER.objects.get(
        codename='views_searchbook',
        content_type=content_type,
    )
    #自定义的下载书本的权限
    permission2 = PER.objects.get(
        codename='views_downloadbook',
        content_type=content_type,
    )
    #添加这两个权限
    user.user_permissions.add(permission1,permission2,)
    #重新载入用户后才能生效
    user = get_object_or_404(User, pk = user_id)
    #验证是否有下载和查询权限
    # print(user.has_perm('app1.views_searchbook')) 
    # print(user.has_perm('app1.views_downloadbook'))

# Create your views here.
def host(request):
    if request.session.get('is_login',None) == True:
        return redirect('/management/')
    else:
        return redirect('/login/')
    
#登录
def login(request):
    if request.session.get('is_login',None) == True:
        return redirect('/management/')
    if request.method == "GET":
        form = My_forms.UserForm
        return render(request, "login.html",{"form":form})
    elif request.method == "POST":
        form = My_forms.UserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            #authenticate
            login_user_obj = auth.authenticate(username = username, password = password)
            if not login_user_obj:
                return render(request, "login.html", {"form": form})
            else:
                request.session["is_login"] = True
                auth.login(request,login_user_obj)
                return redirect('/management/')
        else:
            return render(request, "login.html", {"form": form})

#注册
def register(request):
    if request.method == "GET":
        form = My_forms.RegisterForm
        return render(request, "register.html",{"form":form})
    elif request.method == "POST":
        form = My_forms.RegisterForm(request.POST)
        if form.is_valid():
            username1 = request.POST.get("username1")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            #创建用户
            if password1 == password2:
                if not User.objects.filter(username = username1).first():
                    #用户名查重
                    User.objects.create_user(username = username1,password = password1)
                    userinfo = User.objects.filter(username = username1).first()
                    #print(type(userinfo.id))
                    add_permissions(userinfo.id)
                    return HttpResponse('注册: ' +username1 +' OK!')
                else:
                    error = '用户:'+username1+' 已存在!'
                    return render(request, "register.html", {"form": form,"error":error})
            else:
                error = '未知错误!'
                return render(request, "register.html", {"form": form,"error":error})
        else:
            clear_errors = form.errors.get("__all__")
            return render(request, "register.html", {"form": form,"clear_errors":clear_errors})

#图书后台管理
@login_required
def management(request):
    return render(request,'management.html')

#登出
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/login/')

#录入书本
@login_required
@permission_required('app1.views_addbook',raise_exception=True)
def add_book(request):
    if request.method == "GET":
        form = My_forms.BooksForm
        return render(request, "add_book.html",{"form":form})
    elif request.method == "POST":
        #这里实例表单需要同时传入request.POST和request.FILE 否则FileFied验证一直返回False
        form = My_forms.BooksForm (request.POST,request.FILES)
        if form.is_valid():
            book_name = request.POST.get('book_name')
            book_type = request.POST.get('book_type')
            book_introduction = request.POST.get('book_introduction')
            issue_year = request.POST.get('issue_year')
            book_file = request.FILES.get('book_file')

            if not  models.Books.objects.filter(book_name = book_name).first():
                if book_file:
                    book_file_name = book_file.name
                    #print('文件名：'+book_file_name)111
                    #写入指定位置
                    
                    #在window和linux上自动拼接为windows的 '\\' 或者linux的'/' 
                    BOOK_dir = os.path.join(os.getcwd(),os.sep,'media', book_file_name)
                    with open(BOOK_dir,'wb') as f:
                        for chunk in book_file.chunks():
                            f.write(chunk)
                        f.close()
                    #add_book_time字段取当前时间写入数据库
                    # #authenticate 验证
                    if book_name != None and book_type != None and book_introduction != None and issue_year != None and book_file_name != None:
                        test1 = models.Books(book_name = book_name,book_type = book_type,book_introduction = book_introduction,issue_year = issue_year,book_file_name = book_file_name,add_book_time =str( time.strftime('%Y-%m-%d %H:%M:%S')))
                        test1.save()
                        return HttpResponse('写入数据库成功!')
                    else:
                        return HttpResponse('写入数据库失败!数据缺失!')
                else:
                    return HttpResponse('上传失败!')
            else:
                error = '书本:'+book_name+' 已存在!'
                return render(request, "add_book.html", {"form": form,"error":error})
        else:
            #return HttpResponse('验证失败！')
            return render(request, "add_book.html", {"form": form})

#查询书本(书名查询)
@login_required
@permission_required('app1.views_searchbook',raise_exception=True)
def search_book_by_name(request):
    if request.method == "GET":
        form = My_forms.SearchForm
        return render(request, "search.html",{"form":form})
    elif request.method == "POST":
        form = My_forms.SearchForm (request.POST)
        if form.is_valid():
            book_name = request.POST.get("book_name")
            #print(book_name)
            if book_name:
                res = models.Books.objects.filter(book_name = book_name)
                #print(res)
                if res:
                    book_type_dic = {'1':'Python','2':'C','3':'C++','4':'Java','5':'Javascript','6':'Linux'}
                    dic1 = res[0]
                    dic1.book_type = book_type_dic[dic1.book_type]
                    return render(request,'table.html',{'dic':dic1})
                else:
                    return HttpResponse('没查到数据!')
            else:
                return HttpResponse('查询错误!')
        else:
            return render(request, "search.html", {"form": form})


#删除指定书本以及书本在数据库中的记录
@login_required
def delete_book(request):
    pass

#下载书本
@login_required
@permission_required('app1.views_downloadbook',raise_exception=True)
def download_book(request,book_file_name):
    #在window和linux上自动拼接为windows的 '\\' 或者linux的'/' 
    BOOK_dir = os.path.join(os.getcwd(),os.sep,'media', book_file_name)
    zip_file_name = str(time.time())+'.zip'
    #zip_file_dir = os.getcwd()+'\\media\\tempfiles\\'+zip_file_name
    zip_file_dir = os.path.join(os.getcwd(),os.sep,'media','tempfiles', zip_file_name)
    #为了解决传输中文名的文件时下载后无法显示文件名的问题，决定采取压缩后传输，
    if os.path.isfile(BOOK_dir) ==True:
        z = zipfile.ZipFile(zip_file_dir, 'w', zipfile.ZIP_DEFLATED)
        z.write(BOOK_dir, arcname = book_file_name)
        z.close()
        try:
            f = open(zip_file_dir,'rb')
            response =FileResponse(f)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=' + zip_file_name
            return response
        except:
            return HttpResponse('下载失败!')
    else:
        return HttpResponse('文件不存在!')

#批量导入用户
@login_required
@permission_required('app1.views_addusers',raise_exception=True)
def add_users(request):
    if request.method == "GET":
        form = My_forms.AddUserForm
        return render(request, "add_users.html",{"form":form})
    elif request.method == "POST":
        #这里实例表单需要同时传入request.POST和request.FILE 否则FileFied验证一直返回False
        form = My_forms.AddUserForm (request.POST,request.FILES)
        if form.is_valid():
            user_file = request.FILES.get('user_file')
            if user_file:
                file_name = user_file.name
                #判断是否为xls/xlsx文件,是则继续打开文件解析
                if '.xls' in file_name :
                    temp_file_name = str(time.time()) +'.xls'
                    #linux 和Windows跨平台路劲
                    #user_file_dir = os.getcwd()+'\\temp\\' + temp_file_name
                    user_file_dir = os.path.join(os.getcwd(),os.sep,'temp',temp_file_name)
                    #写入指定位置
                    with open(user_file_dir,'wb') as f:
                        for chunk in user_file.chunks():
                            f.write(chunk)
                        f.close()
                    work_book2 = xlrd.open_workbook (user_file_dir)
                    ws = work_book2.sheet_by_name('Sheet1')
                    if ws.row_values(0) == ['user','password']:
                        msg_list =[]
                        for row in range(1,ws.nrows):
                            for col in range(1,ws.ncols):
                                user1 = ws.cell_value(row,col-1)
                                pass1 = ws.cell_value(row,col)
                                ctype =ws.cell(row,col).ctype
                                if ctype == 2:
                                    pass1 = str(pass1).replace('.0','')
                                if not User.objects.filter(username = user1).first():
                                    #用户名查重
                                    User.objects.create_user(username = user1,password = pass1)
                                    msg = '用户: ' +user1 +' 导入成功!<br>'
                                else:
                                    msg = '用户: ' +user1 +' 已存在，导入失败!<br>'
                                msg_list.append(msg)
                        msgs = ''
                        for msg_info in msg_list:
                            msgs +=msg_info
                        if msgs == '':
                            return HttpResponse('用户表中无数据!')
                        else:
                            return HttpResponse(msgs)
                    else:
                        return HttpResponse('用户表数据格式损坏，请重新上传文件!')   
                elif '.xlsx' in file_name:
                    temp_file_name = str(time.time()) +'.xlsx'
                    user_file_dir = os.path.join(os.getcwd(),os.sep,'temp',temp_file_name)
                    #写入指定位置
                    with open(user_file_dir,'wb') as f:
                        for chunk in user_file.chunks():
                            f.write(chunk)
                        f.close()
                    #打开excel表格
                    work_book2 = xlrd.open_workbook (user_file_dir)
                    ws = work_book2.sheet_by_name('Sheet1')
                    if ws.row_values(0) == ['user','password']:
                        msg_list =[]
                        for row in range(1,ws.nrows):
                            for col in range(1,ws.ncols):
                                user1 = ws.cell(row,col-1)
                                pass1 = ws.cell(row,col)
                                ctype =ws.cell(row,col).ctype
                                if ctype == 2:
                                    pass1 = str(pass1).replace('.0','')
                                if not User.objects.filter(username = user1).first():
                                    #用户名查重
                                    User.objects.create_user(username = user1,password = pass1)
                                    msg = '用户: ' +user1 +'导入成功!\n'
                                else:
                                    msg = '用户: ' +user1 +'已存在，导入失败!\n'
                                msg_list.append(msg)
                        msgs = ''
                        for msg_info in msg_list:
                            msgs +=msg_info
                        if msgs == '':
                            return HttpResponse('用户表中无数据!')
                        else:
                            return HttpResponse(msgs)
                    else:
                        return HttpResponse('用户表数据格式损坏，请重新上传文件!')
                else:
                    error = '上传的文件不是excel文件!请重新上传!'
                    return render(request, "add_users.html", {"form": form,"error":error}) 
            else:
                return HttpResponse('文件不存在!')
        else:
            return render(request, "add_users.html", {"form": form})

#批量导入用户的excel模板
@login_required
@permission_required('app1.views_downloadexcel',raise_exception=True)
def download_excel(rquest):
    #excel_dir = os.getcwd()+'\\testdata\\testdata.zip'
    excel_dir = os.path.join(os.getcwd(),os.sep,'testdata','testdata.zip')
    if os.path.isfile(excel_dir) == True:
        try:
            f = open(excel_dir,'rb')
            response =FileResponse(f)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=' + 'testdata.zip'
            return response
        except:
            return HttpResponse('下载失败!')
    else:
        return HttpResponse('未知异常!')
