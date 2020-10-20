from django.urls import path

from . import views

app_name = 'teams'
urlpatterns = [
    path('invite/', views.SendInvitation.as_view(), name='invite'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('sign_in/<pk>/', views.SingInView.as_view(), name='sign_in'),
    path('invited/<pk>/', views.CheckInvited.as_view(), name='check_invited'),
    path('password_change', views.PasswordChange.as_view(),
         name='password_change'),
    path('password_change_done', views.PasswordChangeDone.as_view(),
         name='password_change_done'),
    path('profile_info/', views.ProfileInfoView.as_view(), name='profile_info'),

    path('team_detail/<int:pk>/', views.TeamView.as_view(), name='team_detail'),
    path('team_edit/<int:pk>/', views.EditProfileView.as_view(), name='team_edit'),
]
