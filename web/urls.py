from django.urls import path

from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),
    # /about/
    path('about/', views.about, name='about'),
    # # ex: /polls/5/
    # path('<int:lang_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:lang_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:lang_id>/vote/', views.vote, name='vote'),
]
