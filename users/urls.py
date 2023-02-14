from django.urls import path, include
from users import views

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('account', views.userAccount, name='account'),
    path('', views.profile, name='profile'),
    path('user-profile/<str:pk>/', views.userProfile, name='profile-users'),

]
