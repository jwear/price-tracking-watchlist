from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login', AccountLoginView.as_view(), name='login'),
    path('logout', AccountLogoutView.as_view(), name='logout'),
    path('register', AccountRegisterView.as_view(), name='register'),
]
