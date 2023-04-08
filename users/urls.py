from django.urls import path, include
from users import views

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('account', views.userAccount, name='account'),
    path('', views.profile, name='profile'),
    path('user-profile/<str:pk>/', views.userProfile, name='profile-users'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('create-skill', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),
    

]
