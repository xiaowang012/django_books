#coding=utf-8
from django.http.response import HttpResponse,FileResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from . import My_forms
from . import models
import time
import os
import zipfile
import xlrd
import random
from functools import wraps

#定义一个全局变量BOOK_NAME用于解决查询书本分页的问题
BOOK_NAME = []

#校验权限的装饰器
def permission_check(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        '''
        校验权限的过程:
        1.装饰器里面每次获取一次session username
        2.根据userid 查询是否为管理员，是则查用户组为admin，否则为others
        3.根据admin/others查询视图set 是否包含传参:views
        4.是则return true  ，否则return 403 
        '''
        #获取用户名
        user_name = request.user
        #获取当前URL
        cur_url = request.path
        #根据用户名查询是否为管理员
        user_info = User.objects.filter(username = user_name).first()
        if user_info:
            is_superuser = int(user_info.is_superuser)
            if is_superuser == 1:
                per_info = models.App1Permission .objects.filter(user_group = 'admin').all()
                if per_info:
                    per_list = []
                    for i in per_info:
                        per_list.append(i.views_func)
                    if cur_url in per_list:
                       return func(request,*args,**kwargs)
                    else:
                        return render(request,'error_403.html')
                else:
                    return render(request,'error_403.html')
            elif is_superuser == 0:
                per_info = models.App1Permission .objects.filter(user_group = 'others').all()
                if per_info:
                    per_list = []
                    for i in per_info:
                        per_list.append(i.views_func)
                    if cur_url in per_list:
                       return func(request,*args,**kwargs)
                    else:
                        return render(request,'error_403.html')
                else:
                    return render(request,'error_403.html')
        else:
            return render(request,'error_403.html')   
    return wrapper

# 127.0.0.1:5000 (仅输入IP+PORT) 判断是否在登录状态
def host(request):
    if request.session.get('is_login',None) == True:
        return redirect('/home/')
    else:
        return redirect('/login/')
    
#用户登录
def login(request):
    # if request.session.get('is_login',None) == True:
        # return redirect('/management/')
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
                #定义密码错误信息
                dic1 = {}
                dic1['message'] = '用户名或密码错误!'
                return render(request, "login.html", {"form": form,"dic1":dic1})
            else:
                request.session["is_login"] = True
                auth.login(request,login_user_obj)
                return redirect('/home/')
                
        else:
            return render(request, "login.html", {"form": form})

#用户注册
def register(request):
    if request.method == "GET":
        form = My_forms.RegisterForm
        return render(request, "register.html",{"form":form})
    elif request.method == "POST":
        form = My_forms.RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            #创建用户
            if password == password1:
                if not User.objects.filter(username = str(username)).first():
                    #用户名查重,如果查不到，正常创建用户
                    try:
                        User.objects.create_user(username = str(username),password = str(password))
                    except:
                        #返回对应的错误提示信息到页面
                        message = ' 注册: ' + str(username) +' Failed!'
                        dic2 = {'frame_type':'alert alert-dismissable alert-danger','title':'ERROR ','message':message}
                        return render(request,'register.html',{'form':form,'dic2':dic2})
                    else:
                        #返回对应的注册成功提示信息到页面
                        message = ' 注册: ' + str(username) +' SUCCESS!'
                        dic2 = {'frame_type':'alert alert-success alert-dismissable','title':'SUCCESS ','message':message}
                        return render(request,'register.html',{'form':form,'dic2':dic2})
                else:
                    error = '用户: '+ str(username) + ' 已存在! 请不要重复注册!'
                    return render(request, "register.html", {"form": form,"error":error})
            else:
                error_msg = '两次输入的密码不一致!'
                return render(request, "register.html", {"form": form,"error":error_msg})
        else:
            #print(form.errors)
            #未通过表单验证
            clear_err = form.errors.get('__all__')
            #print(clear_err)
            if clear_err:
                clear_err = str(clear_err).replace('<ul class="errorlist nonfield"><li>','').replace('</li></ul>','')
            return render(request, "register.html", {"form": form,'clear_err':clear_err})
            
#用户登出
@login_required
@permission_check
def logout(request):
    auth.logout(request)
    return redirect('/login/')

#用户主页
@login_required
@permission_check
def home(request):
    if request.method == 'GET':
        #查询书本的表单
        form = My_forms.SearchBookForm
        #获取当前用户名
        username = request.user
        #print(username)
        #定义前端样式的字典
        dic1 = {'username':username,'active1':'active','active2':'','active3':'',\
        'active4':'','active5':'','current_page_number':1}
        #在book 表中查询书本条目(5条)
        book_info = models.Books.objects.all()[:5]
        #加入每一行数据的的样式到queryset中
        for data in book_info:
            data.style = random.choice(['success','info','warning','error'])
        return render(request,'home.html',{'form':form,'list1':book_info,'dic1':dic1})

#用户主页翻页
@login_required
@permission_check
def home_page(request):
    number = request.GET.get('number')
    #print(number)
    try:
        number = int(number)
    except:
        return HttpResponse('Parameters error')
    else:
        #定义form
        form = My_forms.SearchBookForm()
        #查数据表，设置限制返回的起始值和结束值
        search_start_num = (number-1)*5
        search_end_num = number*5
        #根据页码查询指定数据
        book_info = models.Books.objects.all()[search_start_num:search_end_num]
        #加入每一行数据的的样式到queryset中
        for data in book_info:
            data.style = random.choice(['success','info','warning','error'])
        #渲染到前端
        #获取当前用户名
        username = request.user
        #print(username)
        #定义前端样式的字典
        dic1 = {'username':username,'active1':'','active2':'','active3':'',\
        'active4':'','active5':'','current_page_number':number}
        #根据页码改变分页的样式
        if 1<=number<=5:
            dic1['active'+str(number)] = 'active'
        elif number>5:
            dic1['active_next'] = 'active'
        return render(request,'home.html',{'form':form,'list1':book_info,'dic1':dic1})
        
#用户查询书本(书名查询)
@login_required
@permission_check
def search_book(request):
    #获取url中的页码参数
    num = request.GET.get('num')
    if num:
        try:
            num = int(num)
        except:
            return HttpResponse('参数错误!')
        else:
            if request.method == "POST":
                form = My_forms.SearchBookForm (request.POST)
                if form.is_valid():
                    book_name = request.POST.get("book_name")
                    BOOK_NAME.append(book_name)
                    #查数据
                    book_info = models.Books.objects.filter(book_name = book_name)[0:5]
                    #print(res)
                    if book_info:
                        #获取当前用户名
                        username = request.user
                        #加入每一行数据的的样式到queryset中
                        for data in book_info:
                            data.style = random.choice(['success','info','warning','error'])
                        #定义前端样式的字典
                        dic1 = {'username':username,'active1':'active','active2':'','active3':'',\
                        'active4':'','active5':'','current_page_number':num}
                        #根据页码更改分页效果的样式
                        return render(request,'home_search.html',{'form':form,'dic1':dic1,'list1':book_info})
                    else:
                        #获取当前用户名
                        username = request.user
                        #加入每一行数据的的样式到queryset中
                        for data in book_info:
                            data.style = random.choice(['success','info','warning','error'])
                        #定义前端样式的字典
                        dic1 = {'username':username,'active1':'active','active2':'','active3':'',\
                        'active4':'','active5':'','current_page_number':num}
                        #根据页码更改分页效果的样式
                        return render(request,'home_search.html',{'form':form,'dic1':dic1,'list1':book_info})
                else:
                    #获取当前用户名
                    username = request.user
                    #print(username)
                    #定义前端样式的字典
                    dic1 = {'username':username,'active1':'active','active2':'','active3':'',\
                    'active4':'','active5':'','current_page_number':num}
                    #在book 表中查询书本条目(5条)
                    book_info = models.Books.objects.all()[:5]
                    #加入每一行数据的的样式到queryset中
                    for data in book_info:
                        data.style = random.choice(['success','info','warning','error'])
                    return render(request,'home_search.html',{'form':form,'list1':book_info,'dic1':dic1})
            elif request.method == 'GET':
                form = My_forms.SearchBookForm()
                if len(BOOK_NAME) != 0:
                    #从全局变量中拿查询书本的书名
                    book_name = BOOK_NAME[-1]
                    #根据页码和书名查询对应的信息
                    #查表,定义起始值和结束值
                    search_start_num = (num-1)*5
                    search_end_num = num*5
                    book_info = models.Books.objects.filter(book_name = book_name)[search_start_num:search_end_num]
                    #渲染结果到html
                    #获取当前用户名
                    username = request.user
                    #加入每一行数据的的样式到queryset中
                    for data in book_info:
                        data.style = random.choice(['success','info','warning','error'])
                    #定义前端样式的字典
                    dic1 = {'username':username,'active1':'','active2':'','active3':'',\
                    'active4':'','active5':'','active_next':'','current_page_number':num}
                    #根据页码更改分页效果的样式
                    if 1<=num<=5:
                        dic1['active'+str(num)] = 'active'
                    elif num>5:
                        dic1['active_next'] = 'active'
                    return render(request,'home_search.html',{'form':form,'dic1':dic1,'list1':book_info})
                else:
                    return HttpResponse('参数错误!')

#按类型查询表格翻页
@login_required
@permission_check
def search_by_type(request):  
    #从URL获取书本类型参数和页码
    book_type = request.GET.get('type_1')
    number = request.GET.get('number')
    if book_type:
        try:
            number = int(number)
        except:
            return HttpResponse('参数错误!')
        else:
            form = My_forms.SearchBookForm()
            #根据书本类型和页码查表
            #查表,定义起始值和结束值
            search_start_num = (number-1)*5
            search_end_num = number*5
            book_info = models.Books.objects.filter(book_type = book_type)[search_start_num:search_end_num]
            #渲染结果到html
            #获取当前用户名
            username = request.user
            #加入每一行数据的的样式到queryset中
            for data in book_info:
                data.style = random.choice(['success','info','warning','error'])
            #定义前端样式的字典
            dic1 = {'username':username,'active1':'','active2':'','active3':'',\
            'active4':'','active5':'','active_next':'','current_page_number':number,'type':book_type}
            #根据页码更改分页效果的样式
            if 1<=number<=5:
                dic1['active'+str(number)] = 'active'
            elif number>5:
                dic1['active_next'] = 'active'
            return render(request,'home_search_type.html',{'form':form,'dic1':dic1,'list1':book_info})
    else:
        return HttpResponse('参数错误!')

#录入书本
@login_required
@permission_check
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
                    #print('文件名：'+book_file_name)
                    #写入指定位置
                    #在window和linux上自动拼接为windows的 '\\' 或者linux的'/' 
                    BOOK_dir = os.getcwd() + os.path.join(os.sep,'media', book_file_name)
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

#下载书本
@login_required
@permission_check
def download_book(request):
    #获取book id 参数
    book_id = request.GET.get('code')
    try:
        book_id = int(book_id)
    except:
        return HttpResponse('参数错误!')
    else:
        #根据ID查书本路径
        search_data = models.Books.objects.filter(id = book_id).first()
        if search_data:
            file_name = str(search_data.book_file_name)
            download_number = int(search_data.number_of_downloads)
            #书本存放的位置
            #在window和linux上自动拼接为windows的 '\\' 或者linux的'/' 
            book_file_path = os.getcwd() + os.path.join(os.sep,'media', file_name)
            if os.path.isfile(book_file_path) ==True:
                #利用生成器循环读取文件(20MB一次)
                def read_file(file_path):
                    with open(file_path, 'rb') as targetfile:
                        while True:
                            data = targetfile.read(20*1024*1024)
                            if not data:
                                break
                            yield data
                #传输文件
                try:
                    response =FileResponse(read_file(book_file_path))
                    response['Content-Type']='application/octet-stream'
                    response['Content-Disposition'] = 'attachment;filename=' + file_name
                    #下载成功则更新下载次数
                    download_number += 1
                    #更新下载次数
                    search_data.number_of_downloads = download_number
                    search_data.save()
                    return response
                except:
                    return HttpResponse('下载失败!')     
            else:
                return HttpResponse('文件不存在!')
        else:
            return HttpResponse('书本不存在!')

#管理界面用户管理
@login_required
@permission_check
def user_mgr(request):
    if request.method == 'GET':
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #根据参数查询用户数据，一次10条
        user_info = User.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in user_info:
            #删除多余的字段
            del data.password
            #根据是否为管理员添加group字段(admin/others)
            if data.is_superuser == 1:
                data.group = 'admin'
            elif data.is_superuser == 0:
                data.group = 'others'
            #删除is_superuser字段
            del data.is_superuser
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'user.html',{'user_list':user_info,'dic1':dic1})

#管理界面用户管理翻页
@login_required
@permission_check
def user_page(request):
    number = request.GET.get('number')
    try:
        number = int(number)
    except:
        return HttpResponse('参数错误!')
    else:
        form = My_forms.AddUserForm()
        if request.method == 'GET':
            #查询用户数据
            dic1 = {'active1':'','active2':'','active3':'','active4':'','active5':'',
                    'active_next':'','active_Prev':'','current_page_number':number}
            #根据页码改变分页的样式
            if 1<=number<=5:
                dic1['active'+str(number)] = 'active'
            elif number>5:
                dic1['active_next'] = 'active'
            #根据参数查询用户数据，一次10条
            search_start_num = (number-1)*10
            search_end_num = number*10
            user_info = User.objects.all()[search_start_num:search_end_num]
            #定义样式
            style_list = ['success','info','warning','error']
            for data in user_info:
                #删除多余的字段
                del data.password
                #根据是否为管理员添加group字段(admin/others)
                if data.is_superuser == 1:
                    data.group = 'admin'
                elif data.is_superuser == 0:
                    data.group = 'others'
                #删除is_superuser字段
                del data.is_superuser
                #为表格加随机样式
                data.style = random.choice(style_list)
            return render(request,'user.html',{'user_list':user_info,'dic1':dic1,'form':form})
     
#管理界面用户管理 ：修改用户组(admin切换成others，others切换成admin)
@login_required
@permission_check
def change_group(request):
    userid = request.GET.get('userid')
    group = request.GET.get('group')
    if userid and group:
        if group == 'admin':
            #修改为others
            user_data = User.objects.filter(id = userid).first() 
            if user_data:
                user_data.is_superuser = 0
                user_data.save()
                return redirect('/management/user')
            else:
                return HttpResponse('用户不存在!')
        elif group == 'others':
            user_data = User.objects.filter(id = userid).first()
            if user_data:
                user_data.is_superuser = 1
                user_data.save()
                return redirect('/management/user')
            else:
                return HttpResponse('用户不存在!')
    else:
        return HttpResponse('参数错误!')

#管理界面用户管理 ：删除指定用户
@login_required
@permission_check
def delete_user(request):
    userid = request.GET.get('userid')
    try:
        userid = int(userid)
    except:
        return HttpResponse('参数错误!')
    else:
        user_data = User.objects.filter(id = userid).first() 
        if user_data:
            user_data.delete()
            return redirect('/management/user')
        else:
            return HttpResponse('找不到用户!')

#批量导入用户
@login_required
@permission_check
def add_users(request):
    if request.method == "POST":
        #这里实例表单需要同时传入request.POST和request.FILE 否则FileFied验证一直返回False
        form = My_forms.AddUserForm (request.POST,request.FILES)
        if form.is_valid():
            user_file = request.FILES.get('user_file')
            if user_file:
                file_name = str(user_file.name)
                #判断是否为xls/xlsx文件,是则继续打开文件解析
                if '.xls' in file_name or '.xlsx' in file_name:
                    temp_file_name = str(time.time()) + file_name
                    #linux 和Windows跨平台路径
                    user_file_dir = os.getcwd() + os.path.join(os.sep,'temp',temp_file_name)
                    #写入指定位置
                    with open(user_file_dir,'wb') as f:
                        for chunk in user_file.chunks():
                            f.write(chunk)
                        f.close()
                    work_book2 = xlrd.open_workbook (user_file_dir)
                    ws = work_book2.sheet_by_name('Sheet1')
                    try:
                        line_1_values = ws.row_values(0)
                    except:
                        message = '文件数据为空!'
                        style = 'alert alert-dismissable alert-danger'
                        title = '导入失败! '
                    else:
                        if line_1_values == ['user','password']:
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
                                        msg = '用户: ' + user1 +' 导入成功! '
                                    else:
                                        msg = '用户: ' + user1 +' 已存在，导入失败! '
                                    msg_list.append(msg)
                            #删除excel临时文件
                            if os.path.isfile(user_file_dir) == True:
                                os.remove(user_file_dir)
                            msgs = ''
                            for msg_info in msg_list:
                                msgs +=msg_info
                            if msgs == '':
                                msgs = '用户表中无数据!'
                            #定义消息提醒
                            message = msgs
                            style = 'alert alert-success alert-dismissable'
                            title = '导入成功! '
                        else:
                            message = '用户表数据格式损坏，请重新上传文件!!'
                            style = 'alert alert-dismissable alert-danger'
                            title = '导入失败! '
                else:
                    message = '文件类型错误!'
                    style = 'alert alert-dismissable alert-danger'
                    title = '导入失败! '
            else:
                message = '找不到文件!'
                style = 'alert alert-dismissable alert-danger'
                title = '导入失败! '
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '导入失败! '
        #返回对应的提示信息到前端
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #将提示信息加到dic1中
        dic1['style'] = style
        dic1['title'] = title
        dic1['message'] = message
        #查询用户数据
        user_info = User.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in user_info:
            #删除多余的字段
            del data.password
            #根据是否为管理员添加group字段(admin/others)
            if data.is_superuser == 1:
                data.group = 'admin'
            elif data.is_superuser == 0:
                data.group = 'others'
            #删除is_superuser字段
            del data.is_superuser
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'user.html',{'user_list':user_info,'dic1':dic1,'form':form})

#批量注册用户下载excel模板
@login_required
@permission_check
def download_upload_user_template(request):
    if request.method == 'GET':
        user_template_file = os.getcwd() + os.path.join(os.sep,'media','user_template_file.zip')
        if os.path.isfile(user_template_file) == True:
            try:
                f = open(user_template_file,'rb')
                response =FileResponse(f)
                response['Content-Type']='application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + 'user_template_file.zip'
                return response
            except:
                return HttpResponse('下载失败!')
        else:
            return HttpResponse('模板文件不存在!')
    elif request.method == 'POST':
        return render(request,'error_404.html')

#刷新页面
@login_required
@permission_check
def refresh_permission(request):
    cur_url = request.GET.get('cur_url')
    if cur_url:
        return redirect(cur_url)
    else:
        return HttpResponse('error!')

#管理界面书本管理
@login_required
@permission_check
def book_mgr(request):
    if request.method == 'GET':
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #根据参数查询用户数据，一次10条
        books_info = models.Books.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in books_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'book.html',{'list1':books_info,'dic1':dic1})

#管理界面书本管理页面翻页
@login_required
@permission_check
def book_page(request):
    number = request.GET.get('number')
    try:
        number = int(number)
    except:
        return HttpResponse('参数错误!')
    else:
        form = My_forms.AddUserForm()
        if request.method == 'GET':
            #查询用户数据
            dic1 = {'active1':'','active2':'','active3':'','active4':'','active5':'',
                    'active_next':'','active_Prev':'','current_page_number':number}
            #根据页码改变分页的样式
            if 1<=number<=5:
                dic1['active'+str(number)] = 'active'
            elif number>5:
                dic1['active_next'] = 'active'
            #根据参数查询用户数据，一次10条
            search_start_num = (number-1)*10
            search_end_num = number*10
            books_info = models.Books.objects.all()[search_start_num:search_end_num]
            #定义样式
            style_list = ['success','info','warning','error']
            for data in books_info:
                #为表格加随机样式
                data.style = random.choice(style_list)
            return render(request,'book.html',{'list1':books_info,'dic1':dic1,'form':form})

#管理界面书本管理修改书本信息
@login_required
@permission_check
def update_book(request):
    form = My_forms. UpdateBooksForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            id = request.POST.get('id')
            bookname = request.POST.get('bookname')
            booktype = request.POST.get('booktype')
            book_description = request.POST.get('book_description')
            issue_year = request.POST.get('issue_year')
            file_name = request.POST.get('file_name')
            if id != '':
                book_info = models.Books.objects.filter (id = int(id)).first()
                if book_info:
                    if bookname != '':
                        msg1 = 'book_name'
                        book_info.book_name = str(bookname)
                    else:
                        msg1 =''
                    if booktype != '':
                        msg2 = 'book_type'
                        book_info.book_type = str(booktype)
                    else:
                        msg2 =''
                    if book_description != '':
                        msg3 = 'book_description'
                        book_info.book_introduction = str(book_description)
                    else:
                        msg3 =''
                    if issue_year != '':
                        msg4 = 'issue_year'
                        book_info.issue_year = str(issue_year)
                    else:
                        msg4 = ''
                    if file_name != '':
                        msg5 = 'file_name'
                        book_info.book_file_name = str(file_name)
                    else:
                        msg5 =''
                    book_info.save()
                    mssage_full = msg1 + ' '+msg2+ ' ' + msg3 + ' '+ msg4 + ' '+ msg5
                    if mssage_full == '':
                        message = '修改: None 成功!'
                    else:
                        message = '修改: '+ mssage_full +' 成功!'
                    style = 'alert alert-success alert-dismissable'
                    title = '修改成功! '
                else:
                    message = '用户不存在!'
                    style = 'alert alert-dismissable alert-danger'
                    title = '修改失败! '
            else:
                message = 'id 参数不存在!'
                style = 'alert alert-dismissable alert-danger'
                title = '修改失败! '     
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '修改失败! ' 
        #渲染页面
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #添加提示信息到dic1
        dic1['message'] = message
        dic1['style'] = style
        dic1['title'] = title
        #根据参数查询用户数据，一次10条
        books_info = models.Books.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in books_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'book.html',{'list1':books_info,'dic1':dic1,'form':form})
    
#管理界面书本管理删除书本信息
#删除指定书本以及书本在数据库中的记录
@login_required
@permission_check
def delete_book(request):
    #获取book id 参数
    book_id = request.GET.get('id')
    try:
        book_id = int(book_id)
    except:
        return HttpResponse('参数错误!')
    else:
        #根据ID查书本路径
        search_data = models.Books.objects.filter(id = book_id).first()
        if search_data:
            file_name = str(search_data.book_file_name)
            #书本存放的位置
            #在window和linux上自动拼接为windows的 '\\' 或者linux的'/' 
            book_file_path = os.getcwd() + os.path.join(os.sep,'media', file_name)
            if os.path.isfile(book_file_path) == True:
                os.remove(book_file_path)
            #删除数据库这一条的数据
            search_data.delete()
            return redirect('/management/book/')
        else:
            return HttpResponse('书本不存在!')

#管理界面书本管理添加书本
@login_required
@permission_check
def add_book(request):
    if request.method == 'POST':
        form = My_forms.AddBooksForm(request.POST,request.FILES)
        if form.is_valid():
            bookname = request.POST.get('bookname')
            booktype = request.POST.get('booktype')
            book_description = request.POST.get('book_description')
            issue_year = request.POST.get('issue_year')
            bookfile = request.FILES.get('bookfile')
            if bookname and booktype != "None" and book_description and issue_year and bookfile:
                #接收文件.获取文件名
                file_name = str(bookfile.name)
                #linux 和Windows跨平台路径
                book_file_dir = os.getcwd() + os.path.join(os.sep,'media',file_name)
                #写入指定位置
                with open(book_file_dir,'wb') as f:
                    for chunk in bookfile.chunks():
                        f.write(chunk)
                #将书本文件压缩删除源文件
                zipped_file_name = str(time.time()) + '.zip'
                zipped_path = os.getcwd() + os.path.join(os.sep,'media',zipped_file_name)
                with zipfile.ZipFile(zipped_path, 'w', zipfile.ZIP_DEFLATED) as zf:        
                    zf.write(book_file_dir,arcname = file_name)
                #压缩完成后删除源文件
                if os.path.isfile(book_file_dir) == True:
                    os.remove(book_file_dir)
                # #写入数据库
                data = models.Books(id = None ,book_name = bookname,book_type = booktype,book_introduction = book_description,\
                    issue_year=issue_year,book_file_name = zipped_file_name,add_book_time=time.strftime('%Y-%m-%d %H:%M:%S'),\
                    number_of_downloads=0)
                data.save()
                #添加成功，返回成功的消息
                message = '添加书本: ' + bookname + ' 成功!'
                style = 'alert alert-success alert-dismissable'
                title = '导入成功! '
            else:
                #参数不全
                message = '添加书本: ' + bookname + ' 失败!'
                style = 'alert alert-dismissable alert-danger'
                title = '导入失败! '
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '导入失败! '
        
        #print(message)
        #渲染页面
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #将报错提示加到dic1里面
        dic1['message'] = message
        dic1['style'] = style
        dic1['title'] = title
        #根据参数查询用户数据，一次10条
        books_info = models.Books.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in books_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'book.html',{'list1':books_info,'dic1':dic1,'form':form})

#管理界面系统权限管理
@login_required
@permission_check
def system_mgr(request):
    if request.method == 'GET':
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #根据参数查询用户数据，一次10条
        permissions_info = models.App1Permission. objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in permissions_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'system.html',{'list1':permissions_info,'dic1':dic1})

#管理界面系统管理页面翻页
@login_required
@permission_check
def system_page(request):
    number = request.GET.get('number')
    try:
        number = int(number)
    except:
        return HttpResponse('参数错误!')
    else:
        form = My_forms.AddUserForm()
        if request.method == 'GET':
            #查询用户数据
            dic1 = {'active1':'','active2':'','active3':'','active4':'','active5':'',
                    'active_next':'','active_Prev':'','current_page_number':number}
            #根据页码改变分页的样式
            if 1<=number<=5:
                dic1['active'+str(number)] = 'active'
            elif number>5:
                dic1['active_next'] = 'active'
            #根据参数查询用户数据，一次10条
            search_start_num = (number-1)*10
            search_end_num = number*10
            permissions_info = models.App1Permission .objects.all()[search_start_num:search_end_num]
            #定义样式
            style_list = ['success','info','warning','error']
            for data in permissions_info:
                #为表格加随机样式
                data.style = random.choice(style_list)
            return render(request,'system.html',{'list1':permissions_info,'dic1':dic1,'form':form})

#管理界面系统管理页面添加permission
@login_required
@permission_check
def add_permission(request):
    if request.method == 'POST':
        form = My_forms.AddPermissionForm(request.POST)
        if form.is_valid():
            group_name = request.POST.get('group_name')
            url = request.POST.get('url')
            description = request.POST.get('description')
            if group_name and url and description:
                #写入数据库
                data = models.App1Permission (id = None ,user_group = group_name,views_func = url,description = description)
                data.save()
                #添加成功，返回成功的消息
                message = '添加权限: (' + group_name + ' '+ url +' '+ description+') 成功!'
                style = 'alert alert-success alert-dismissable'
                title = '添加成功! '
            else:
                #参数不全
                message = '添加权限:  失败!'
                style = 'alert alert-dismissable alert-danger'
                title = '添加失败! '
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '添加失败! '
        
        #print(message)
        #渲染页面
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #将报错提示加到dic1里面
        dic1['message'] = message
        dic1['style'] = style
        dic1['title'] = title
        #根据参数查询用户数据，一次10条
        permission_info = models.App1Permission .objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in permission_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'system.html',{'list1':permission_info,'dic1':dic1,'form':form})

#管理界面系统管理页面修改permission
@login_required
@permission_check
def update_permission(request):
    form = My_forms.UpdatePermissionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            id = request.POST.get('id')
            group_name1 = request.POST.get('group_name')
            url1 = request.POST.get('url')
            description1 = request.POST.get('description')
            if id != '':
                permission_info = models.App1Permission .objects.filter (id = int(id)).first()
                if permission_info:
                    if group_name1 != '':
                        msg1 = 'group_name'
                        permission_info.user_group = str(group_name1)
                    else:
                        msg1 =''
                    if url1 != '':
                        msg2 = 'url'
                        permission_info.views_func = str(url1)
                    else:
                        msg2 =''
                    if description1 != '':
                        msg3 = 'description'
                        permission_info.description = str(description1)
                    else:
                        msg3 =''
                    permission_info.save()
                    mssage_full = msg1 + ' '+msg2+ ' ' + msg3 + ' '
                    if mssage_full == '':
                        message = '修改: None 成功!'
                    else:
                        message = '修改: '+ mssage_full +' 成功!'
                    style = 'alert alert-success alert-dismissable'
                    title = '修改成功! '
                else:
                    message = '用户不存在!'
                    style = 'alert alert-dismissable alert-danger'
                    title = '修改失败! '
            else:
                message = 'id 参数不存在!'
                style = 'alert alert-dismissable alert-danger'
                title = '修改失败! '     
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '修改失败! ' 
        #渲染页面
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #添加提示信息到dic1
        dic1['message'] = message
        dic1['style'] = style
        dic1['title'] = title
        #根据参数查询用户数据，一次10条
        permission_info = models.App1Permission .objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in permission_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'system.html',{'list1':permission_info,'dic1':dic1,'form':form})


#管理界面系统管理页面删除permission
@login_required
@permission_check
def delete_permission(request):
    #获取book id 参数
    permission_id = request.GET.get('id')
    try:
        permission_id = int(permission_id)
    except:
        return HttpResponse('参数错误!')
    else:
        #根据ID查书本路径
        search_data = models.App1Permission .objects.filter(id = permission_id).first()
        if search_data:
            #删除数据库这一条的数据
            search_data.delete()
            return redirect('/management/system/')
        else:
            return HttpResponse('permission不存在!')


#管理界面系统管理页面批量导入permission
@login_required
@permission_check
def upload_permissions(request):
    if request.method == "POST":
        #这里实例表单需要同时传入request.POST和request.FILE 否则FileFied验证一直返回False
        form = My_forms.UploadPermissionForm (request.POST,request.FILES)
        if form.is_valid():
            permission_file = request.FILES.get('permission_file')
            if permission_file:
                file_name = str(permission_file.name)
                #判断是否为xls/xlsx文件,是则继续打开文件解析
                if '.xls' in file_name or '.xlsx' in file_name:
                    temp_file_name = str(time.time()) + file_name
                    #linux 和Windows跨平台路径
                    permission_file_dir = os.getcwd() + os.path.join(os.sep,'temp',temp_file_name)
                    #写入指定位置
                    with open(permission_file_dir,'wb') as f:
                        for chunk in permission_file.chunks():
                            f.write(chunk)
                        f.close()
                    work_book2 = xlrd.open_workbook (permission_file_dir)
                    ws = work_book2.sheet_by_name('Sheet1')
                    try:
                        line_1_values = ws.row_values(0)
                    except:
                        message = '文件数据为空!'
                        style = 'alert alert-dismissable alert-danger'
                        title = '导入失败! '
                    else:
                        if line_1_values == ['user_group','url','description']:
                            msg_list =[]
                            for row in range(1,ws.nrows):
                                try:
                                    row_values_1 = ws.row_values(row)
                                    user_group = str(row_values_1[0])
                                    url = str(row_values_1[1])
                                    description = str(row_values_1[2])
                                except:
                                    msg = ' 第 '+str(row) + '行数据错误! '
                                else:
                                    #写入数据库
                                    data = models.App1Permission(id = None,user_group = user_group,\
                                        views_func = url,description = description)
                                    data.save()
                                    msg = ' 权限: (' + user_group +' ' + url +' '+ description +') 导入成功! '
                                msg_list.append(msg)
                            #删除excel临时文件
                            if os.path.isfile(permission_file_dir) == True:
                                os.remove(permission_file_dir)
                            msgs = ''
                            for msg_info in msg_list:
                                msgs +=msg_info
                            if msgs == '':
                                msgs = '用户表中无数据!'
                            #定义消息提醒
                            message = msgs
                            style = 'alert alert-success alert-dismissable'
                            title = '导入成功! '
                        else:
                            message = '用户表数据格式损坏，请重新上传文件!!'
                            style = 'alert alert-dismissable alert-danger'
                            title = '导入失败! '
                else:
                    message = '文件类型错误!'
                    style = 'alert alert-dismissable alert-danger'
                    title = '导入失败! '
            else:
                message = '找不到文件!'
                style = 'alert alert-dismissable alert-danger'
                title = '导入失败! '
        else:
            message = form.errors.as_text()
            style = 'alert alert-dismissable alert-danger'
            title = '导入失败! '
        #返回对应的提示信息到前端
        #查询用户数据
        dic1 = {'active1':'active','active2':'','active3':'','active4':'','active5':'',
                'active_next':'','active_Prev':'','current_page_number':1}
        #将提示信息加到dic1中
        dic1['style'] = style
        dic1['title'] = title
        dic1['message'] = message
        #查询用户数据
        permission_info = models.App1Permission.objects.all()[0:10]
        #定义样式
        style_list = ['success','info','warning','error']
        for data in permission_info:
            #为表格加随机样式
            data.style = random.choice(style_list)
        return render(request,'system.html',{'list1':permission_info,'dic1':dic1,'form':form})


#批量导入permission下载excel模板
@login_required
@permission_check
def download_upload_permission_template(request):
    if request.method == 'GET':
        permission_template_file = os.getcwd() + os.path.join(os.sep,'media','permission_template_file.zip')
        if os.path.isfile(permission_template_file) == True:
            try:
                f = open(permission_template_file,'rb')
                response =FileResponse(f)
                response['Content-Type']='application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + 'permission_template_file.zip'
                return response
            except:
                return HttpResponse('下载失败!')
        else:
            return HttpResponse('模板文件不存在!')
    elif request.method == 'POST':
        return render(request,'error_404.html')
    
