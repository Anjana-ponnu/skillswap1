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
    path("admin_index/", views.admin_index, name="admin_index"),
    path("admin_users/", views.admin_users, name="admin_users"),
    path("admin_skills/", views.admin_skills, name="admin_skills"),
    path("admin_sessions/", views.admin_sessions, name="admin_sessions"),
    path("admin_reviews/", views.admin_reviews, name="admin_reviews"),
    path("admin_analytics/", views.admin_analytics, name="admin_analytics"),
    path("admin_settings/", views.admin_settings, name="admin_settings"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path("logout/", views.logout, name="logout"),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit_skill/<str:skill_name>/', views.edit_skill, name='edit_skill'),
    path('delete_skill/<str:skill_name>/', views.delete_skill, name='delete_skill'),
]


