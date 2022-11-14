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

    # /compare/lang1/lang2
    #path('<str:lang1>/<str:lang2>/', views.detail, name='detail')
    # /compare/
    path('compare/', views.compare, name='compare'),

    # /reference/
    # path('compare/', controller.for.reference???, name='reference'),
    # /reference/lang1/
    path('reference/', views.reference, name='reference'),

    # API reference
    # /api/{structure}/{lang}/{version}
    path('api/<str:structure_key>/<str:lang>/<str:version>/', views.api_reference, name='api.reference'),

    # API compare
    # /api/{structure}/{lang1}/{version1}/{lang2}/{version2}
    path('api/<str:structure_key>/<str:lang1>/<str:version1>/<str:lang2>/<str:version2>/', views.api_compare, name='api.compare'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
