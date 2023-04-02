from django.urls import path

from .views import BookListCreateView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book_list_create'),
    path('/<int:pk>', BookListCreateView.as_view(), name='book_retrieve_update_destroy'),
]
