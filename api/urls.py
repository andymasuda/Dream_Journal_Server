from django.urls import path
from . import views

urlpatterns = [
    path('entries/', views.EntriesListView.as_view()),
    path('entries/<int:id>/', views.EntriesDetailView.as_view()),
]