"""my_life_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from my_life import (
    views
)
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='angular_home.html')),
    path('home', TemplateView.as_view(template_name='angular_home.html')),
    path('gallery', TemplateView.as_view(template_name='angular_home.html')),
    path('posts', TemplateView.as_view(template_name='angular_home.html')),
    path('login', TemplateView.as_view(template_name='angular_home.html')),
    path('posts/<str:id>', TemplateView.as_view(template_name='angular_home.html')),
    path('gallery/<str:id>', TemplateView.as_view(template_name='angular_home.html')),
    path('v1/login', views.login),
    path('v1/gallery', views.get_gallery),
    path('v1/gallery/<str:id>', views.get_image),
    path('v1/gallery/<str:id>/next', views.get_next_image),
    path('v1/gallery/<str:id>/previous', views.get_previous_image),
    path('v1/home', views.get_home_posts),
    path('v1/posts/<str:id>', views.get_post),
    path('v1/posts', views.get_posts)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
