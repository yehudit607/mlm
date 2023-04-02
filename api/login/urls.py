from django.urls import path

from api.login.views import login_view

urlpatterns = [
    path('', login_view, name='login'),
]
