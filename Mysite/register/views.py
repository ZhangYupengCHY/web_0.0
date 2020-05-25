from django.shortcuts import render
from register.models import Userlogin
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django.core.mail import send_mail


# Create your views here.


def send_register_mail(recept_email,username):
    """
    用户登录时，发送邮件
    单发邮件:send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
    群发邮件:send_mass_mail()
    :param request:
    :return:
    """
    subject = '恭喜你注册成功...'
    message = '很高兴{}你成为XX的一员,blah blah blah.'.format(username)
    from_mail = '1579922399@qq.com'
    recipient_list = [recept_email]
    # register_message1 = (subject,message,from_mail,recipient_list)
    try:
        send_mail(
            subject, message, from_mail, recipient_list
        )
        return 'success'
    except Exception as e:
        print(e)
        return 'fail'


def register(request):
    """
    注册的函数,将用户注册的一些信息上传到数据库中
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        realname = request.POST.get('realname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        city = request.POST.get('city')

        print(username)
        # 保存信息到数据库
        Userlogin.objects.create(username=username, password=password, realname=realname, email=email, phone=phone,
                                 birthday=birthday, gender=gender, city=city)

        send_mail_status = send_register_mail(email,username)
        if send_mail_status == 'success':
            print('用户注册: <用户> {} <注册成功>.'.format(username))
            return HttpResponseRedirect("/login/")
        else:
            print('用户注册: <用户> {} <注册失败>.'.format(username))
            return Http404

    return render_to_response('register.html', locals())
