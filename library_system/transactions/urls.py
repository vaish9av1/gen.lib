from django.urls import path
from .views import checkout_view, issue_list_view, return_book_view

app_name = 'transactions'

urlpatterns = [
    path('checkout/<int:book_id>/', checkout_view, name='checkout'),
    path('issues/', issue_list_view, name='issue_list'),
    path('issues/return/<int:issue_id>/', return_book_view, name='return_book'),
]