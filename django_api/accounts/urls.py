from django.urls import path
from . import views

# Login at /api-token-auth
# Sign-up at /
urlpatterns = [
    path('', views.create_user, name='register'),
    path('login/', views.login, name='login'),
]
