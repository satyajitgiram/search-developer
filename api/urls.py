from django.urls import path, include
from api import views


urlpatterns = [


    path('routes/',views.getRoutes),
    path('projects/',views.getProjects),
    path('project/<str:pk>/',views.getProject),

]

