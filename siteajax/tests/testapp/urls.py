from django.urls import path

from . import views

urlpatterns = [
    path('sample_view_1/', views.sample_view_1),
    path('sample_view_2/', views.sample_view_2),
    path('sample_view_3/', views.SampleView3.as_view()),
]
