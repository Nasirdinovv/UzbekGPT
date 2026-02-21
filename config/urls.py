
from django.contrib import admin
from django.urls import path
# from django import views
from umumiy.views import login_user,index, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('chat/', views.chat_view, name='chat'),
    path('login_user/', login_user, name='login_user'),
    path('', index, name='index'),
    path('logout_user/', logout_user, name='logout_user'),
]

