from django.urls import path, include
from app import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='home'),
    path('add/',views.addProject, name='add_project'),
    path('single/<str:id>',views.singleProject, name='single_project'),
    path('edit/<str:id>',views.editProject, name='edit_project'),
    path('delete/<str:id>',views.deleteProject, name='delete_project'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
