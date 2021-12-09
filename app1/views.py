#coding=utf-8
from django.http.response import HttpResponse,FileResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_exempt, csrf_protect
from . import My_forms
from . import models
import time
import os
import zipfile


# Create your views here.
def host(request):
    return redirect('/login/')
    # dic1 = {'code':200,'mothed':'get'}
    # return JsonResponse(dic1)
    
#登录
def login(request):
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
#@csrf_exempt
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
                    
                    BOOK_dir = os.getcwd()+'\\media\\' + book_file_name
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

#批量录入书本(excel)
@login_required
def batch_upload_book(request):
    pass

#查询书本(书名查询)
@login_required
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
def download_book(request,book_file_name):
    BOOK_dir = os.getcwd()+'\\media\\' + str(book_file_name)
    zip_file_name = str(time.time())+'.zip'
    zip_file_dir = os.getcwd()+'\\media\\tempfiles\\'+zip_file_name
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





