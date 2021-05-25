from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sample_1/', views.sample_1, name='sample_1'),
]
