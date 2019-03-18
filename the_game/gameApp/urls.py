from django.urls import path
from . import views

app_name = 'gameApp'

urlpatterns = [
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('gameplay', views.GameplayView.as_view(), name='gameplay'),
    path('gameplay/check_answer', views.check_answer, name='check_answer'),
    path('topten', views.ToptenView.as_view(), name='topten'),
]
