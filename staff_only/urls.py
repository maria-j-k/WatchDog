from django.urls import path

from . import views

app_name = 'staff_only'
urlpatterns = [
    path(
        'clients/',
        views.ClientListView.as_view(),
        name='clients'),
    path(
        'client/<int:pk>/',
        views.ClientDetailView.as_view(),
        name='client_detail'),
    path(
        'compositions/',
        views.CompositionListView.as_view(),
        name='compositions'),
    path(
        'composition_add/',
        views.CompositionAdd.as_view(),
        name='composition_add'),
    path(
        'composition/<int:pk>/',
        views.CompositionDetailView.as_view(),
        name='composition_detail'),
    path(
        'composition_edit/<int:pk>/',
        views.CompositionEditView.as_view(),
        name='composition_edit'),
    path(
        'composition/delete/<int:pk>/',
        views.CompositionDeleteView.as_view(),
        name='composition_delete'),
    path(
        'ascriptions/',
        views.AscriptionListView.as_view(),
        name='ascriptions'),
    path(
        'ascription_add/',
        views.AscriptionAddView.as_view(),
        name='ascription_add'),
    path(
        'ascriptions/<int:pk>/',
        views.ClientAscriptionView.as_view(),
        name='client_ascriptions'),
    path(
        'manage_ascriptions/<int:pk>/',
        views.ManageAscriptionsView.as_view(),
        name='manage_ascriptions'),
]