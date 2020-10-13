from django.urls import path

from . import views

app_name = 'training'
urlpatterns = [
    path('<int:pk>/', views.HomeView.as_view(), name='profile'),
    path('location/', views.LocationView.as_view()),
    path('exercise_add/<int:pk>/', views.ExerciseAddView.as_view(), name='exercise_add'),
    path('exercise_detail/<int:pk>/', views.AscriptionDetailView.as_view(), name='exercise_detail'),
]
