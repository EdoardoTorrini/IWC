from django.urls import path
from . import views

app_name = "mail"

urlpatterns = [
    path('check_login/', views.CheckLogin.as_view(), name='check_login'),
    path('home/', views.HomeMailView.as_view(), name='home'),
    path('login/', views.LoginMailView.as_view(), name='login'),
    path('inspect_mail/', views.MailInspector.as_view(), name='inspect_mail'),
]
