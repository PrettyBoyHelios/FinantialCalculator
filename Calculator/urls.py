from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('alt/', views.alternatives_list, name="alternatives"),
    path('alt/create/', views.create_alternative, name="create_alternative"),
    path('alt/edit/<int:id>/', views.edit_alternative, name="edit_alternative"),
    path('alt/comparing/add/<int:id>/', views.select_for_compare, name="select_for_compare"),
    path('alt/comparing/remove/<int:id>/', views.unselect_for_compare, name="unselect_for_compare"),
    path('alt/comparing/result/', views.compare, name="compare"),
    path('convert/', views.conversions, name="conversions"),
    path('interest/', views.interest_conversions, name="interest_conversions"),
    path('interest/result/', views.interest_showconversions, name="show_interest"),
    path('periods/', views.number_periods, name="number_periods"),
]