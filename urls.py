"""
URL configuration for skillswap_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path("user_index/", views.user_index, name="user_index"),
    path("home/", views.home, name="home"),
    path("auth/", views.auth, name="auth"),
    path("save_user/", views.save_user, name="save_user"),
    path("chklogin/", views.chklogin, name="chklogin"),
    path("logout/", views.logout, name="logout"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("follow_user/<int:user_id>/", views.follow_user, name="follow_user"),
    path('settings/', views.settings_view, name='settings'),
    path('help/', views.help_view, name='help'),
    path('bookmark/<int:post_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('my_learning/', views.my_learning_view, name='my_learning'),
    path('my_skills/', views.my_skills_view, name='my_skills'),
    path('saved_posts/', views.saved_posts_view, name='saved_posts'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comments/', views.get_post_comments, name='get_post_comments'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]
