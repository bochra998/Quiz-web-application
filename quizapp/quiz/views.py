import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from quiz.forms import UserForm, LoginForm, utiliForm, QuestionForm
from .models import Questions, Users
import paho.mqtt.client as paho

# Create your views here.

def ofhome(request):
    return render(request, 'quiz/OfficialHome.html', locals())

def home(request):
    choices = Questions.CAT_CHOICES
    print(choices)
    return render(request,
        'quiz/home.html',
        {'choices':choices})

def adminpage(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('quiz:adminpage')
    else:
        return render(request,'AddQuestion.html',locals())

def questions(request , choice):
    print(choice)
    ques = Questions.objects.filter(catagory__exact = choice)
    return render(request,
        'quiz/questions.html',
        {'ques':ques})

def on_publish(client,userdata,result):
    print("data published \n")
    pass

def result(request):
    print("result page")
    if request.method == 'POST':
        global score,total
        data = request.POST
        datas = dict(data)
        qid = []
        qans = []
        ans = []

        score = 0
        for key in datas:
            try:
                qid.append(int(key))
                qans.append(datas[key][0])
            except:
                print("Csrf")
        for q in qid:
            ans.append((Questions.objects.get(id = q)).answer)

        total = len(ans)
        for i in range(total):
            if ans[i] == qans[i]:
                score += 1
        print(score)
        file = open('C:\\Users\\Lenovo\\Desktop\\result.txt','w')
        file.write(str(score)+'\\'+str(total))
        file.close()
        broker = "192.168.1.106"
        port = 1883
        client1 = paho.Client("control1")  # create client object
        client1.on_publish = on_publish  # assign function to callback
        client1.connect(broker, port)  # establish connection
        client1.publish("result/result1", 'your score is : '+str(score)+'\\'+str(total))
    return render(request,
        'quiz/result.html',
                  {'score': score,
                   'total': total}
                  )


def login_page_Admin(request):
    if request.method == "POST":
        form9 = LoginForm(data=request.POST or None)
        if form9.is_valid():
            username = form9.cleaned_data['username']
            password = form9.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('quiz:adminpage')
        else:
            print(form9.errors)
    else:
        form9 = LoginForm(data=request.POST or None)

    return render(request, 'registration/LoginAdmin.html', locals())

def register_user(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = utiliForm(request.POST or None)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            u_form.save()
            username = u_form.cleaned_data.get('username')
            password = u_form.cleaned_data.get('password')
            userauth = authenticate(username=username, password=password)
            login(request, userauth)
            return  redirect('quiz:login_user')

    else:
        u_form = UserForm(request.POST)
        p_form = utiliForm(request.POST)
    return render(request, 'registration/register_user.html', {'u_form': u_form, 'p_form': p_form})

def login_page_user(request):
    if request.method == "POST":
        form8 = AuthenticationForm(data=request.POST or None)
        if form8.is_valid():
            user = form8.get_user()
            login(request, user)
            return redirect('quiz:home')
        else:
            print(form8.errors)
    else:
        form8 = AuthenticationForm(data=request.POST or None)

    return render(request, 'registration/loginUser.html', locals())