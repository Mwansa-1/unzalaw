from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
import static

urlpatterns = [
    path("", views.index, name = "index"),
    path('cart/', views.view_cart, name='view_cart'),
    path('borrow_books/', views.borrow_books, name='borrow_books'),
    path('results/', views.results, name='results'),
    path('view_borrowing_history/', views.view_borrowing_history, name='view_borrowing_history'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]