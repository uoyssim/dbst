from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import UpdateDev
from .models import Log
from .models import Dev
from .models import Actor

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
    temp.save()
    return HttpResponseRedirect('/wireless/')

def signal(request):
    addr = request.META['REMOTE_ADDR']
    Log.objects.create(dev = addr)
    if not Dev.objects.get(pk = addr):
        Dev.objects.create(id = addr)
    else :
        temp = Dev.objects.get(pk = addr)
        temp.last_log = timezone.now();
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

