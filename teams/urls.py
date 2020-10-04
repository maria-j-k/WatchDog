from django.urls import path

from . import views

app_name = 'teams'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout', views.LogoutUserView.as_view(), name='logout'),
    path('sign_in/', views.SingInView.as_view(), name='sign_in'),
    path('profile_info/', views.ProfileInfoView.as_view(), name='profile_info'),
    path('team_detail/<int:pk>/', views.TeamView.as_view(), name='team_detail'),
]
