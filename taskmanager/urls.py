"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Main import views as mainView
from Users import views as userView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainView.home,name='home'),
    path('home/',mainView.home,name='home'),
    path('register/',userView.registerNewUser,name='register'),
    path('login/', LoginView.as_view(template_name='Users/login.html'), name='login'), #using Django's built in feature for Login
    path('logout/', LogoutView.as_view(template_name='Users/logout.html'), name='logout'), 
    path('ViewUserTasks/',mainView.ViewUserTasks,name = "view_tasks"), 
    path('EditTasks',mainView.EditTasks,name="edit_tasks"),
    path('markTaskFinished/',mainView.task_mark_status_complete,name="markTaskComplete"),
    path('teams/<str:team_name>',mainView.teams,name='teams'),
    path('profile/<str:user_name>',mainView.profile,name='profile')    
]
