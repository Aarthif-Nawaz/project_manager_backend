from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserView.as_view(), name="main"),
    path('project/', views.ProjectView.as_view(), name="project")
]