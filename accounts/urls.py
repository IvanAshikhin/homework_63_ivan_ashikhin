from django.urls import path

from accounts.views import LoginView, logout_view, RegisterView, ProfileView, UserChangeView
from posts.views import SubscribeView

urlpatterns =[
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/change', UserChangeView.as_view(), name='change'),
    path('subscribe/<int:pk>/', SubscribeView.as_view(), name='subscribe'),
]