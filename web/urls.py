"""Urls provided by codethesaur.us"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),

    # /robots.txt
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),  #add the robots.txt file

    # /about/
    path('about/', views.about, name='about'),

    # legacy url path
    path('compare/', views.concepts, name='compare'),

    # legacy url path
    path('reference/', views.concepts, name='reference'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
