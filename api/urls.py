from django.urls import path
from . import views

urlpatterns = [
    path('entries/', views.EntriesListView.as_view()),
    path('entries/<int:id>/', views.EntriesDetailView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('users/<int:id>/', views.UserDetailView.as_view())
]