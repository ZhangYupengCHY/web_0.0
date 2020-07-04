from django.shortcuts import render
from django.shortcuts import HttpResponse
from django_pandas.managers import DataFrameManager
import pandas as pd
from django_pandas.io import read_frame
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from login.models import Userlogin
from datetime import datetime
from datetime import timedelta


# Create your views here.

# 路由转发用户请求到视图函数。视图函数处理用户请求，也就是编写业务处理逻辑


# 得到用户名单
def getUserInfo():
    userInfo = Userlogin.objects.all()
    userInfo = read_frame(userInfo)
    return userInfo


def login(request):
    if request.method == 'POST':
        request.get_signed_cookie()
        loginUserName = request.POST.get('username')
        loginPassword = request.POST.get('password')

        userInfo = getUserInfo()

        userNamepassWord = [(str(userName), str(passWord)) for userName, passWord in
                            zip(userInfo['username'], userInfo['password'])]
        if (loginUserName, loginPassword) in userNamepassWord:
            # 登录成功后将用户名保存在session中
            request.session['username'] = loginUserName
            request.session['is_login'] = True
            # 两个月过期
            expiry_dyas = 60
            expiry_seconds = expiry_dyas*24*3600
            request.session.set_expiry(expiry_seconds)
            return HttpResponseRedirect("/home/")

        else:
            error_msg = '用户名或是密码不正确，请重新输入账号密码.若没有账号，请'

    return render_to_response('login.html', locals())
