from django.urls import path

from . import views

urlpatterns = [
    path('sample_view_1/', views.sample_view_1),
]
