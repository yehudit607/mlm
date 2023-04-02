from django.urls import path

from .views import UserListCreateView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('/<int:pk>', UserListCreateView.as_view(), name='user_retrieve_update_destroy'),
]
