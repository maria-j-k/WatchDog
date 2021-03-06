from django.urls import path

from . import views

app_name = 'staff_only'
urlpatterns = [
    path(
        'staff/',
        views.StaffListView.as_view(),
        name='list_staff'),
    path('staff_add/',
         views.MakeStaff.as_view(),
         name='make_staff'),
    path('edit_staff/<int:pk>/',
         views.EditStaffMember.as_view(),
         name='edit_staff'),
    path('strip_staff_status/<int:pk>/',
         views.StripStaffStatus.as_view(),
         name='strip_staff_status'),
#    path(
#        'clients/',
#        views.ClientListAll.as_view(),
#        name='clients'),
    path(
        'training_clients/',
         views.ClientListTraining.as_view(),
         name='training_clients'),
    path(
        'need_ascription/',
         views.ClientsNeedAscription.as_view(),
         name='need_ascription'),
    path(
        'registered_users/',
         views.RegisteredPersons.as_view(),
         name='registered_users'),
    path(
        'invited_people/',
        views.ListInvited.as_view(),
         name='invited_people'),
    path('delete_invited/<pk>/',
         views.DeleteInvited.as_view(),
         name='delete_invited'),
    path(
        'suspended_clients/',
         views.SuspendedClients.as_view(),
         name='suspended_clients'),
    path(
        'client/<int:pk>/',
        views.ClientDetailView.as_view(),
        name='client_detail'),
    path(
        'toggle_active/<int:pk>/',
        views.ToggleActive.as_view(),
        name='toggle_active'),
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
        'ascription_add/',
        views.AscriptionAddView.as_view(),
        name='ascription_add'),
    path(
        'ascriptions/<int:pk>/',
        views.ClientAscriptionView.as_view(),
        name='client_ascriptions'),
    path('ascriptions_toggle/<int:pk>/<int:comp_pk>/',
         views.ToggleAscriptionView.as_view(),
         name='toggle_ascription'),
    path(
        'manage_ascriptions/<int:pk>/',
        views.ManageAscriptionsView.as_view(),
        name='manage_ascriptions'),
]

