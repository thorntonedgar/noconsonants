from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api-docs/', views.api_docs, name='api_docs'),
    path('built-with/', views.built_with, name='built_with'),
]

