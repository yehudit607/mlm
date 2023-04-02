from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path('users', include('api.users.urls')),
    re_path('books', include('api.books.urls')),
    re_path('checkouts', include('api.checkouts.urls')),
    re_path('login', include('api.login.urls')),

]
