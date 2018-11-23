from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('alt/', views.alternatives_list, name="alternatives"),
    path('alt/create/', views.create_alternative, name="create_alternative"),
    path('convert/', views.conversions, name="conversions"),
    path('interest/', views.interest_conversions, name="interest_conversions"),
    path('interest/result/', views.interest_showconversions, name="show_interest"),
    path('periods/', views.number_periods, name="number_periods")
]