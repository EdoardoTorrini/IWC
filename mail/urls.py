from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "mail"

urlpatterns = [
    path('check_login/', views.CheckLogin.as_view(), name='check_login'),
    path('home/', views.HomeMailView.as_view(), name='home'),
    path('login/', views.LoginMailView.as_view(), name='login'),
    path('inspect_mail/', views.MailInspector.as_view(), name='inspect_mail'),
    path('send_email/', views.MailSender.as_view(), name='send_email'),
    path('downloadFile/', views.DownloadFile.as_view(), name='downloadFile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
