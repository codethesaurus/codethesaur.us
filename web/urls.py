from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    # /
    path('', views.index, name='index'),

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

]
