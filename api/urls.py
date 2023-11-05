from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('routes/',views.getRoutes),
    path('projects/',views.getProjects),
    path('project/<str:pk>/',views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote, name='project-vote'),
    path('remove-tag/', views.removeTag, name='remove-tag')

]

