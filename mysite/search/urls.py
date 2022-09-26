from django.urls import path

from . import views


app_name = 'search'
urlpatterns = [
    # ex: /search/
    path('', views.index, name='index'),
    # ex: /search/results/
    path('results/', views.results, name='results'),
    path('two/', views.searchtwo, name='two'),
]