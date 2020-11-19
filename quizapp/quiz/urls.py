from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from . import views

app_name ="quiz"

urlpatterns = [
    path("",views.ofhome, name="ofhome"),
    path("home/", views.home, name="home"),
    path("result/", views.result, name='result'),
    path("login_Admin/", views.login_page_Admin, name="login_Admin"),
    path("register_user/", views.register_user, name="register_user"),
    path("login_user/", views.login_page_user, name="login_user"),
    path("adminpage/", views.adminpage, name="adminpage"),
    path("<choice>/",views.questions,name="questions"),
    path("<choice>/result", views.result, name="resuresu"),
]
