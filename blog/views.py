from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Max, Avg, Count
import pytz
from .forms import UpdateDev
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import LoginForm, SignUpForm
from datetime import datetime, timedelta
# import sendgrid
import os


# from sendgrid.helpers.mail import *

def group(request):
    if request.user.is_authenticated():
        try:
            my_groups = Group_auth.objects.filter(user=AuthUser.objects.get(username=request.user.username))
        except:
            my_groups = None
        if my_groups is not None:
            my_group_list = Group.objects.filter(group_id__in=my_groups.values_list('group_id', flat=True))
            group_list = Group.objects.exclude(group_id__in=my_group_list)
            print(my_group_list.query)
            print(group_list.query)
            return render(request, 'blog/group.html', {'group_list': group_list, 'my_group_list': my_group_list})
        else:
            group_list = Group.objects.all()
            print(group_list.query)
            return render(request, 'blog/group.html', {'group_list': group_list})
    else:
        group_list = Group.objects.all()
        print(group_list.query)
        return render(request, 'blog/group.html', {'group_list': group_list})


def group_create(request):
    return render(request, 'blog/group_create.html', {})


def group_create_db(request):
    if request.method == "POST":
        group = Group.objects.create(group_name=request.POST.get('group_name', None),
                                     group_info=request.POST.get('group_info', None), like=0)
        user = AuthUser.objects.get(username=request.user.username)
        Group_auth.objects.create(user=user, group=group, auth='A')
    return redirect('/group/')


def group_in(request, groupID):
    try:
        auth = Group_auth.objects.filter(group=Group.objects.get(group_id=groupID)).get(
            user=AuthUser.objects.get(username=request.user.username))
    except:
        auth = None
    group = Group.objects.get(group_id=groupID)
    if auth is None:
        mummy = Movie.objects.get(title_kor="미이라")
        mummy_trailer = Trailer.objects.get(movie=mummy)
        return render(request, 'blog/index.html', {'mummy': mummy, 'mummy_trailer': mummy_trailer})

    posting = Posting.objects.filter(group = group)
    return render(request, 'blog/group_in.html', {'auth': auth, 'group': group, 'posting': posting})

def group_post(request, postingID):
    post = Posting.objects.get(posting_id=postingID)
    post.count = post.count + 1

    group = Group.objects.get(group_id=post.group.group_id)
    posting = Posting.objects.get(posting_id=postingID)
    try:
        comments = Posting_comment.objects.filter(posting=posting)
    except:
        comments = None

    try:
        auth = Group_auth.objects.filter(group = group).get(user=AuthUser.objects.get(username = request.user.username))
    except:
        auth = None
    if auth is None:
        mummy = Movie.objects.get(title_kor="미이라")
        mummy_trailer = Trailer.objects.get(movie=mummy)
        return render(request, 'blog/index.html', {"mummy": mummy, "mummy_trailer": mummy_trailer})
    else:
        if comments is None:
            return render(request, 'blog/group_post.html',
                          {'post': post, 'group': group, 'auth': auth})
        else:
            return render(request, 'blog/group_post.html',
                          {'post': post, 'group': group, 'comments': comments, 'auth': auth})


def group_comment(request):
    if request.method == "POST":
        groupID = request.POST.get('groupID', None)
        Posting_comment.objects.create(
            posting=Posting.objects.get(posting_id=request.POST.get('postID', None)),
            user=AuthUser.objects.get(username=request.user.username),
            comment=request.POST.get('comment', None))

        post = Posting.objects.get(posting_id=request.POST.get('postID', None))
        group = Group.objects.get(group_id=groupID)
        try:
            comments = Posting_comment.objects.filter(
                posting=Posting.objects.get(posting_id=request.POST.get('postID', None)))
        except:
            comments = None
        try:
            auth = Group_auth.objects.filter(group_id=group.group_id).get(user_id=request.user.id)
        except:
            auth = None
        return render(request, 'blog/group_post.html',
                      {'post': post, 'group': group, 'comments': comments, 'auth': auth})
    else:
        return redirect('group')


def group_write(request, groupID):
    return render(request, 'blog/group_write.html', {'groupID': groupID})


def group_write_db(request):
    if request.method == "POST":
        groupID = request.POST.get("groupID", None)
        group_ = Group.objects.get(group_id=groupID)
        Posting.objects.create(user=AuthUser.objects.get(username=request.user.username),
                                   group=group_, title=request.POST.get("title", None),
                                   contents=request.POST.get("contents", None), count=0, like=0)
        try:
            posting = Posting.objects.filter(group_id=groupID)
        except:
            posting = None
        try:
            auth = Group_auth.objects.filter(group_id=groupID).get(user_id=request.user.id)
            print(auth.query)
        except:
            auth = None

        return render(request, 'blog/group_in.html', {'auth': auth, 'group': group, 'posting': posting})
    else:
        return redirect('group')


def group_join(request, groupID):
    user = AuthUser.objects.get(username=request.user.username)

    group = Group.objects.get(group_id=groupID)

    Group_auth.objects.create(user=user, group=group, auth='N')
    try:
        auth = Group_auth.objects.filter(group_id=groupID).get(user_id=request.user.id)
    except:
        auth = None
    try:
        posting = Posting.objects.get(group_id=groupID)
    except:
        posting = None
    if posting is None:
        return render(request, 'blog/group_in.html', {'auth': auth, 'group': group})
    else:
        return render(request, 'blog/group_in.html', {'auth': auth, 'group': group, 'posting': posting})


def recommend(request):
    if request.user.is_authenticated():
        user = AuthUser.objects.get(username=request.user.username)
        print(user)
        try:
            user_inter = UserInterest.objects.filter(user=user)
            print(user_inter)
        except:
            user_inter = None

        newest = Movie.objects.exclude(movie_id__in=user_inter.values_list('movie', flat=True)).order_by('-playdate')[
                 :5]
        print(newest.query)

        one_week_ago = datetime.today() - timedelta(days=7)
        hot = UserInterest.objects.filter(timestamp__gte=one_week_ago).values('movie').annotate(
            count=Count('movie')).order_by('-count')
        hotest = Movie.objects.filter(movie_id__in=hot.values_list('movie', flat=True))
        print(hotest.query)

        today = datetime.today()
        print(today.month)
        print(today.day)
        try:
            release_today = Movie.objects.filter(playdate__month=today.month).filter(playdate__day=today.day)
            print(release_today.query)
        except:
            release_today = None
        if release_today is not None:
            return render(request, 'blog/recommend.html',
                          {'user': user, 'newest': newest, 'hotest': hotest[0], 'release': release_today[0]})
        else:
            return render(request, 'blog/recommend.html',
                          {'user': user, 'newest': newest, 'hotest': hotest[0], 'release': release_today})
    else:
        recommends = Movie.objects.all().order_by('playdate')[:5]
        print(recommends.query)
        one_week_ago = datetime.today() - timedelta(days=7)
        hot = UserInterest.objects.filter(timestamp__gte=one_week_ago).values('movie').annotate(
            count=Count('movie')).order_by('-count')
        hotest = Movie.objects.filter(movie_id__in=hot.values_list('movie', flat=True))

        return render(request, 'blog/recommend.html', {'recommens': recommends, 'hotest': hotest[0]})


def index(request):
    mummy = Movie.objects.get(title_kor="미이라")
    mummy_trailer = Trailer.objects.get(movie=mummy)
    return render(request, 'blog/index.html', {'mummy': mummy, 'mummy_trailer': mummy_trailer})


def dev_info(request):
    devs = Dev.objects.all()
    return render(request, 'blog/dev_info.html', {'devs': devs})


def log(request):
    logs = Log.objects.all()
    return render(request, 'blog/log.html', {'logs': logs})


def log_setting(request):
    devs = Dev.objects.all();
    return render(request, 'blog/log_setting.html', {'devs': devs})


def actor_info(request, actorID):
    if request.method == "POST":
        temp = ActorScore.objects.create(user=AuthUser.objects.get(username=request.user.username),
                                         actor=Actor.objects.get(actor_id=actorID), score=0)
        temp.score = int(request.POST.get('score', None))
        temp.save()

        # temp = Actor.objects.get(pk = actorID)
        # print(temp.name)
        # print(int(request.POST.get('score',None)))
        # temp.score = temp.score + int(request.POST.get('score',None))
        # temp.save()
        mummy = Movie.objects.get(title_kor="미이라")
        mummy_trailer = Trailer.objects.get(movie=mummy)
        return render(request, 'blog/index.html', {"mummy": mummy, "mummy_trailer": mummy_trailer})

    temp = Actor.objects.get(pk=actorID)
    scoreTemp = ActorScore.objects.filter(actor_id=actorID)
    scoreAVG = 0
    hasVoteRight = True
    for i in scoreTemp:
        if i.user_id == request.user.id:
            hasVoteRight = False
        scoreAVG += i.score
    if scoreAVG > 0:
        scoreAVG /= scoreTemp.count()
    roleTemp = Role.objects.filter(actor=actorID)
    movieTemp = Movie.objects.filter(movie_id__in=roleTemp.values_list('movie', flat=True))
    if request.user.is_authenticated():
        user = AuthUser.objects.get(username=request.user.username)
        count = temp.count + 1
        temp.count = count
        temp.save()
    return render(request, 'blog/actor_info.html',
                  {'actor': temp, 'scores': scoreTemp, 'voteRight': hasVoteRight, 'avg': scoreAVG,
                   'roles_and_movies': zip(roleTemp, movieTemp)})


def movie_info(request, movieID):
    if request.method == "POST":
        temp = Score.objects.create(user=AuthUser.objects.get(username=request.user.username),
                                    movie=Movie.objects.get(movie_id=movieID), score=0)
        # request.user.userid
        temp.score = int(request.POST.get('score', None))
        temp.save()
        mummy = Movie.objects.get(title_kor="미이라")
        mummy_trailer = Trailer.objects.get(movie=mummy)
        return render(request, 'blog/index.html', {"mummy": mummy, "mummy_trailer": mummy_trailer})

    temp = Movie.objects.get(pk=movieID)
    scoreTemp = Score.objects.filter(movie_id=movieID)
    scoreAVG = 0
    hasVoteRight = True
    for i in scoreTemp:
        if i.user_id == request.user.id:
            hasVoteRight = False
        scoreAVG += i.score
    if scoreAVG > 0:
        scoreAVG /= scoreTemp.count()
    genreTemp = Genre.objects.filter(movie_id=movieID)
    trailerTemp = Trailer.objects.filter(movie=movieID)
    directTemp = Direct.objects.filter(movie_id=movieID)
    directorTemp = Director.objects.filter(director_id__in=directTemp.values_list('director', flat=True))
    roleTemp = Role.objects.filter(movie=movieID)
    actorTemp = Actor.objects.filter(actor_id__in=roleTemp.values_list('actor', flat=True))
    if request.user.is_authenticated():
        try:
            user = AuthUser.objects.get(username=request.user.username)
            interest = UserInterest.objects.get(user_id=user)
        except:
            interest = None
        if interest is None:
            UserInterest.objects.create(user=user, movie_id=movieID)
    return render(request, 'blog/movie_info.html',
                  {'movie': temp, 'scores': scoreTemp, 'voteRight': hasVoteRight, 'avg': scoreAVG, 'genres': genreTemp,
                   'trailers': trailerTemp,
                   'directors': directorTemp, 'roles_and_actors': zip(roleTemp, actorTemp)})


def director_info(request, directorID):
    temp = Director.objects.get(pk=directorID)
    print(temp.query)
    directTemp = Direct.objects.filter(director=directorID)
    print(directTemp.query)
    movieTemp = Movie.objects.filter(movie_id__in=directTemp.values_list('movie_id', flat=True))
    print(movieTemp.query)
    if request.user.is_authenticated():
        user = AuthUser.objects.get(username=request.user.username)
        count = temp.count + 1
        temp.count = count
        temp.save()
    return render(request, 'blog/director_info.html', {'director': temp, 'movies': movieTemp})


def search(request):
    if request.POST.get('name', None) is None:
        return render(request, 'blog/search.html', {})
    else:
        actorTemp = Actor.objects.filter(name__contains=request.POST.get('name', None))
        movieTemp = Movie.objects.filter(title_kor__contains=request.POST.get('name', None))
        directorTemp = Director.objects.filter(name__contains=request.POST.get('name', None))
        if actorTemp.count() + movieTemp.count() + directorTemp.count() > 0:
            return render(request, 'blog/search.html',
                          {'actors': actorTemp, 'movies': movieTemp, 'directors': directorTemp})
        else:
            return render(request, 'blog/search.html', {})


def board_write(request):
    return render(request, 'blog/board_write.html', {})


def QA_create_db(request):
    if request.method == "POST":
        q = QA.objects.create(category=request.POST.get('category', None),
                              user=AuthUser.objects.get(username=request.user.username),
                              qa_title=request.POST.get('title', None), qa_contents=request.POST.get('context', None),
                              state='A');
        print(q.query)
    return redirect('/qna_list/')


def QA_reply_db(request):
    if request.method == "POST":
        post = QA.objects.get(qa_id=request.POST.get("qa_id", None))
        post.QA_contents = request.POST.get("contents", None)
        post.state = request.POST.get("state", None)
        post.save()
    qa_list = QA.objects.all()
    auth = True
    return render(request, 'blog/qna_list.html', {'qa_list': qa_list, 'auth': auth})


def on_off(request, devId):
    print(devId)
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
    Log.objects.create(dev=addr)
    try:
        t = Dev.objects.get(pk=addr)
    except Dev.DoesNotExist:
        t = None
    if t == None:
        Dev.objects.create(id=addr, setting=0, mail_sent=0)
    else:
        temp = Dev.objects.get(pk=addr)
        temp.last_log = timezone.now();
        if temp.setting == 0:
            if temp.mail_sent == 0:
                time_ = temp.last_log.astimezone(pytz.timezone('Asia/Seoul'))
                time_ = time_.__format__("%Y %m %d %H:%M:%S")
                sendMail("%s �ְ�ħ��" % (temp.info),
                         "%s �ְ� ħ�� �߻�����: %s \n\nħ�� �ð�: %s" % (temp.info, temp.addr, time_))
                temp.mail_sent = 1
        else:
            temp.mail_sent = 0
        temp.save()
    return HttpResponse(status=204)


def givemelogs(request):
    return HttpResponse(serializers.serialize('json', Log.objects.all()), content_type='json')


def getDevInfo(request):
    devID = request.GET.get('devID', None)
    print(devID)
    return JsonResponse(Dev.objects.get(pk=devID))


def update(request):
    if request.method == "POST":
        temp = Dev.objects.get(pk=request.POST.get('id', None))
        temp.info = request.POST.get('info', None)
        temp.addr = request.POST.get('addr', None)
        temp.setting = request.POST.get('setting', None)
        temp.save()
    return redirect('/wireless/')


def sendMail(subject, content_string):
    print("���� ����")
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("admin@gotong.org")
    to_email = Email("jjgjoojis@gmail.com");
    content = Content("text/plain", content_string)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def check(request):
    devs = Dev.objects.all();
    for dev in devs:
        log = dev.last_log
        diff = datetime.strptime(timezone.now().__format__("%Y %m %d %H:%M:%S"),
                                 "%Y %m %d %H:%M:%S") - datetime.strptime(log.__format__("%Y %m %d %H:%M:%S"),
                                                                          "%Y %m %d %H:%M:%S")
        diff_min = diff.seconds
        if diff_min >= dev.setting and dev.setting > 0 and dev.mail_sent == 0:
            sendMail('���! �������� �����ϴ�.',
                     "%s ���� %d �ð����� �������� �����ϴ�.\n\n�ּ�: %s" % (dev.info, dev.setting, dev.addr))
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

    elif request.method == "GET":
        userform = SignUpForm()
    return render(request, "registration/signup.html", {"userform": userform})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request)
            return redirect('registration/login.html')
        else:
            return HttpResponse('�α��� ����. �ٽ� �õ��غ�����.')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def moviemate(request):
    trailer = Trailer.objects.all()
    trailer = trailer[:20]
    actor = Actor.objects.all()
    actor = actor[:20]
    director = Director.objects.all()
    director = director[:20]
    return render(request, 'blog/moviemate.html', {'trailer': trailer, 'actor': actor, 'director': director})


def userinfo(request):
    if request.user.is_authenticated():
        username = AuthUser.objects.get(username=request.user.username)
        try:
            info = UserInfo.objects.get(id=request.user.username)
        except:
            info = None
        if request.method == "POST":
            if info is None:
                q = UserInfo.objects.create(id=request.user.username, birthday=request.POST.get("user_birth", None),
                                            email=request.POST.get("email", None),
                                            phone=request.POST.get("phone", None))
                print(q.query)
            else:
                info.birthday = request.POST.get("user_birth", None)
                info.email = request.POST.get("email", None)
                info.phone = request.POST.get("phone", None)
                info.save()
                mummy = Movie.objects.get(title_kor="미이라")
                mummy_trailer = Trailer.objects.get(movie=mummy)
            return render(request, "blog/index.html", {'mummy': mummy, 'mummy_trailer': mummy_trailer})
        else:
            if info is not None:
                return render(request, 'blog/user_info.html', {'info': info})
            else:
                return render(request, 'blog/user_info.html', {'info': info})


def qna_list(request):
    if request.user.is_authenticated():
        try:
            current_user = AuthUser.objects.get(username=request.user.username)
        except:
            current_user = None
        if current_user.is_superuser == 1:
            auth = True
            try:
                qa_list = QA.objects.all().order_by('-timestamp')
            except:
                qa_list = None
        else:
            auth = False
            try:
                qa_list = QA.objects.filter(user=current_user).order_by('-timestamp')
            except:
                qa_list = None
        return render(request, 'blog/qna_list.html', {'qa_list': qa_list, 'auth': auth})
    else:
        return render(request, 'blog/qna_list.html', {})


def qa_post(request, qa_id):
    try:
        current_user = AuthUser.objects.get(username=request.user.username)
    except:
        current_user = None
    if current_user.is_superuser == 1:
        auth = True
    else:
        auth = False
    post = QA.objects.get(qa_id=qa_id)
    return render(request, 'blog/qa_post.html', {'post': post, 'auth': auth})
