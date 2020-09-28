from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('api-token-auth/', views.login, name='login'),
]
