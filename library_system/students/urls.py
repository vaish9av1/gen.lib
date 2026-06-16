from django.urls import path
from .views import student_list_view, student_create_view, student_update_view

app_name = 'students'

urlpatterns = [
    path('', student_list_view, name='student_list'),
    path('add/', student_create_view, name='student_create'),
    path('edit/<int:pk>/', student_update_view, name='student_update'),
]