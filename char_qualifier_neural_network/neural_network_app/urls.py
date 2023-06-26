from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('upload/', views.upload_image, name='upload_image'),
    path('train/', views.train_network, name='train_network'),
    path('process/', views.process_image, name='process_image'),
    path('train_progress/', views.train_progress, name='train_progress')
]

