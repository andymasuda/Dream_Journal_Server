from django.urls import path
from . import views

urlpatterns = [
    path('entries/', views.EntryListView.as_view()),
    path('entries/<int:id>/', views.EntryDetailView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('users/<int:id>/', views.UserDetailView.as_view()),
    path('images/', views.DreamImagesView.as_view()),
    path('login/', views.TokenView.as_view())

    
]