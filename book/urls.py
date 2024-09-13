
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('donate_book/', views.donate_book, name='donate_book'),
    path('book_detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book_download/<int:pk>/', views.book_download, name='book_download'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('my_donations/', views.MyDonations.as_view(), name='my_donations'),
    path('update_book/<int:pk>/', views.update_book, name='update_book'),
    path('search/', views.search, name='search'),

    # file upload
    path('upload/', views.convert_file, name='convert_file'),

    




    
]


