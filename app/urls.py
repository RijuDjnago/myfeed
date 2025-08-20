from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('auth/', views.login_signup_view, name='auth'),
    path('profile/', views.profile_view, name="profile")
]