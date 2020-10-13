from django.urls import path

from . import views

app_name = 'training'
urlpatterns = [
    path('exercises/<int:pk>', views.HomeView.as_view(), name='exercises'),
    path('exercise_add/<int:pk>/', views.ExerciseAddView.as_view(), name='exercise_add'),
    path('exercise_detail/<int:pk>/', views.AscriptionDetailView.as_view(), name='exercise_detail'),
    # path('ascription_add', views.AscriptionAddView.as_view(), name='ascription_add'),
    
]
