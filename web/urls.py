"""Urls provided by codethesaur.us"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    # legacy url path
    path('compare/', views.concepts, name='compare'),

    # legacy url path
    path('reference/', views.concepts, name='reference'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
