from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from . import views

urlpatterns = [
    # Sign-up at /
    path('', views.create_user, name='register'),
    # Login at login/
    path('login/', views.login, name='login'),
    # path('register_new/', views.register_new, name='reg'),

    # Check history at /login_history/<user_id>
    path('login_history/<str:user_id>', views.history_view, name='history'),
]
