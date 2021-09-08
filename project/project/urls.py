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
from os import name
from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from accounts import views as accounts_views
from events import views
from django.contrib.auth import views as auth_views
from categories import views as cat_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.Home.as_view(), name='home'),
    re_path(r'^all_events/$', views.AllEvents.as_view(), name='all_events'),
    
    re_path(r'^event/(?P<pk>\d+)/$', views.OneEvent.as_view(), name='event'),
    re_path(r'^new_event/$', views.NewEvent.as_view(), name='new_event'),
    re_path(r'^event/(?P<pk>\d+)/new_reply/$', views.NewReply.as_view(), name='new_reply'),
    

    re_path(r'^signup/$', accounts_views.SignUp.as_view(), name='signup'),
    re_path(r'^registry/$', accounts_views.Registry.as_view(), name='registry'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^account/(?P<id>\d+)/$', accounts_views.Account.as_view(), name='account'),


    re_path(r'^categories/$', cat_views.Categories.as_view(), name='categories'),
    re_path(r'^category/(?P<id>\d+)/$', cat_views.OneCategory.as_view(), name='category'),

# password change
    re_path(r'^password_change/$', 
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),
    re_path(r'^password_change/done/$', 
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_done'),

#password reset
    path('', include('django.contrib.auth.urls')),#important
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),


#edit urls
    path('event/<int:pk>/reply/<int:id>/edit/',
        views.UpdateReplyView.as_view(), name='edit_reply'),
    path('event/<int:pk>/edit/',
        views.UpdateEventView.as_view(), name='edit_event'), 
    path('account/<int:id>/edit/',
        accounts_views.UpdateProfileView.as_view(), name='edit_profile'), 
    path('account/<int:id>/followers/', 
        accounts_views.FollowersView.as_view(), name='followers'),

    path('profiles/', 
        accounts_views.ProfilesView.as_view(), name='profiles'),

    path('liked_events/', accounts_views.LikedEventsView.as_view(), name='liked_events'),
    path('would_like_to_attend_events/', accounts_views.WouldLikeToAttendView.as_view(), 
        name='wlt_attend_events'),
    path('event/<int:pk>/appreciation/', views.AppreciationView.as_view(), name='appreciation'),

    path('like/', views.LikeButtonAjax.as_view(), name='like'),
    path('attend/', views.AttendButtonAjax.as_view(), name='attend'),
    path('follow/', accounts_views.FollowButtonAjax.as_view(), name='follow'),

    path('search/', views.SearchResultsView.as_view(), name='search_results'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
