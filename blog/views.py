from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import pytz
from .forms import UpdateDev
from .models import Log
from .models import Dev

from .models import Actor

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import LoginForm, SignUpForm

#from datetime import datetime, timedelta import sendgrid
import os
#from sendgrid.helpers.mail import *

def group(request):
    return render(request, 'blog/group.html', {})
def index(request):
    return render(request, 'blog/index.html', {})

def dev_info(request):
    devs = Dev.objects.all()
    return render(request, 'blog/dev_info.html', {'devs': devs})

def log(request):
    logs = Log.objects.all()
    return render(request, 'blog/log.html', {'logs': logs})

def log_setting(request):
    devs = Dev.objects.all();
    return render(request, 'blog/log_setting.html', {'devs': devs})

def actor_info(request):
	actors = Actor.objects.all()
	return render(request, 'blog/actor_info.html', {'actors': actors})

def on_off(request, devId):
    print (devId)
    temp = Dev.objects.get(pk=devId)
    if temp.setting == 0:
        temp.setting = 24
    else:
        temp.setting = 0
    temp.mail_sent = 0
    
    temp.save()
    return HttpResponseRedirect('/wireless/')

def signal(request):
    addr = request.META['REMOTE_ADDR']
    Log.objects.create(dev = addr)
    try:
        t = Dev.objects.get(pk = addr)
    except Dev.DoesNotExist:
        t = None
    if t == None:
        Dev.objects.create(id = addr, setting = 0, mail_sent = 0)
    else :
        temp = Dev.objects.get(pk = addr)
        temp.last_log = timezone.now();
        if temp.setting == 0:
            if temp.mail_sent == 0:
                time_ = temp.last_log.astimezone(pytz.timezone('Asia/Seoul'))
                time_ = time_.__format__("%Y %m %d %H:%M:%S")
                sendMail("%s 주거침입"%(temp.info),"%s 주거 침입 발생지역: %s \n\n침입 시간: %s"%(temp.info, temp.addr,time_ ))
                temp.mail_sent = 1
        else:
            temp.mail_sent = 0
        temp.save()
    return HttpResponse(status=204)

def givemelogs(request):
    return HttpResponse(serializers.serialize('json', Log.objects.all()), content_type='json')

def getDevInfo(request):
    devID = request.GET.get('devID', None)
    print (devID)
    return JsonResponse(Dev.objects.get(pk = devID))

def update(request):
    if request.method == "POST":
        print(request.POST)
        temp = Dev.objects.get(pk = request.POST.get('id',None))
        temp.info = request.POST.get('info',None)
        temp.addr = request.POST.get('addr',None)
        temp.setting = request.POST.get('setting',None)
        temp.save()

    return redirect('/wireless/')

def sendMail(subject, content_string):
    print("메일 보냄!")
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("admin@gotong.org")
    to_email = Email("jjgjoojis@gmail.com");
    content = Content("text/plain", content_string)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def check(request):
    devs = Dev.objects.all();
    for dev in devs :
        log = dev.last_log
        diff = datetime.strptime(timezone.now().__format__("%Y %m %d %H:%M:%S"), "%Y %m %d %H:%M:%S") - datetime.strptime(log.__format__("%Y %m %d %H:%M:%S"), "%Y %m %d %H:%M:%S")
        diff_min = diff.seconds
        if diff_min >= dev.setting and dev.setting > 0 and dev.mail_sent == 0:
            sendMail('경고! 움직임이 없습니다.', "%s 님이 %d 시간동안 움직임이 없습니다.\n\n주소: %s"%(dev.info, dev.setting, dev.addr))
            dev.mail_sent = 1
            dev.save()

    return HttpResponse(status=200); 


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username__exact=username).count():
            return HttpResponse('duplicate id', 400)
        else:
            user = User.objects.create_user(username, password=password)
            user.first_name = request.POST.get('name', '')
            user.save()
            return render(request, "registration/signup_next.html")

    elif request.method =="GET":
        userform = SignUpForm()
    return render(request, "registration/signup.html", {"userform": userform})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request)
            return redirect('registration/login.html')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})