from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('alt/', views.alternatives_list, name="alternatives"),
    path('alt/create/', views.create_alternative, name="create_alternative"),
]