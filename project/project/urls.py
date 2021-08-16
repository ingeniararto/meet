"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from accounts import views as accounts_views
from events import views
from django.contrib.auth import views as auth_views
from categories import views as cat_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.Home.as_view(), name='home'),
    re_path(r'^all_events/$', views.AllEvents.as_view(), name='all_events'),
    
    re_path(r'^event/(?P<pk>\d+)/$', views.OneEvent.as_view(), name='event'),
    re_path(r'^new_event/$', views.NewEvent.as_view(), name='new_event'),
    re_path(r'^event/(?P<pk>\d+)/new_reply/$', views.NewReply.as_view(), name='new_reply'),
    re_path(r'^event/(?P<pk>\d+)/appreciation/$', views.Appreciation.as_view(), name='appreciation'),
    

    re_path(r'^signup/$', accounts_views.SignUp.as_view(), name='signup'),
    re_path(r'^registry/$', accounts_views.Registry.as_view(), name='registry'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^account/(?P<id>\d+)/$', accounts_views.Account.as_view(), name='account'),


    re_path(r'^categories/$', cat_views.Categories.as_view(), name='categories'),
    re_path(r'^category/(?P<id>\d+)/$', cat_views.OneCategory.as_view(), name='category'),

# password change
    re_path(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    re_path(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),



]
