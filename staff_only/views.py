from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (DeleteView, DetailView, ListView, UpdateView,
        View)

from .forms import (AscribeCompositionForm, AscriptionForm, ComposeForm,
FieldForm, MakeStaffForm)
from .models import Ascription, Composition
from teams.models import Invited, User


class StaffListView(UserPassesTestMixin, ListView):
    """Displays all staff members who has not admin status."""
    def test_func(self):
        return self.request.user.is_staff
    model = User
    template_name = 'staff_only/staff_list.html'
    queryset = User.objects.filter(is_staff=True, is_superuser=False)


class MakeStaff(UserPassesTestMixin, View):
    """Allows to change the status of a user and accord staff privileges."""
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        form = MakeStaffForm()
        return render(request, 'staff_only/make_staff_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MakeStaffForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            return redirect(reverse('staff_only:list_staff'))
        return render(request, 'staff_only/make_staff_form.html', {'form': form})


#class ClientListAll(ListView):
#    """Displays list of all clients with some basic information attached."""
#    model = User
#    template_name ='staff_only/user_list.html'
#    queryset = User.objects.filter(is_staff=False)


class ClientListTraining(UserPassesTestMixin, ListView):
    """Displays list of clients who has already exercises ascribed."""
    def test_func(self):
        return self.request.user.is_staff

    model = User
    template_name = 'staff_only/training_list.html'
    queryset = User.objects.filter(ascription__isnull=False, is_active=True).distinct()



class ClientsNeedAscription(UserPassesTestMixin, ListView):
    """Displays all active users with full profile, who has no exercises
    ascribed yet or whose ascriptions has been anulated."""
    def test_func(self):
        return self.request.user.is_staff

    model = User
    template_name = 'staff_only/need_ascription.html'
    queryset = User.objects.filter(_has_full_profile=True,
                                   ascription__isnull=True,
                                   is_staff=False)


class RegisteredPersons(UserPassesTestMixin, ListView):
    """Displays all person, who has created an account, but didn't fill out their
    profile."""
    def test_func(self):
        return self.request.user.is_staff

    model = User
    template_name = 'staff_only/registered_persons.html'
    queryset = User.objects.filter(_has_full_profile=False, is_staff=False)


class ListInvited(UserPassesTestMixin, ListView):
    """Displays all invited people who had not register yet."""
    def test_func(self):
        return self.request.user.is_staff

    model = Invited 
    template_name = 'staff_only/invited.html'
    queryset = Invited.objects.all()


class SuspendedClients(UserPassesTestMixin, ListView):
    """Displays all clients who has been suspended but not deleted"""
    def test_func(self):
        return self.request.user.is_staff

    model = User
    template_name = 'staff_only/suspended_clients.html'
    queryset = User.objects.filter(is_active=False)




class ClientDetailView(UserPassesTestMixin, DetailView):
    """Displays detailed information about a client."""
    def test_func(self):
        return self.request.user.is_staff

    model = User
    template_name ='staff_only/user_detail.html'


class ToggleActive(PermissionRequiredMixin, View):
    permission_required = 'c_can_toggle'
    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next')
        print(next_url)
        user = User.objects.get(pk=kwargs['pk'])
        user.toggle_active()
        return redirect(next_url)


class CompositionListView(UserPassesTestMixin, ListView):
    """Displays list of all compositions with the names of clients, if the composition is ascribed to any client.
    """
    def test_func(self):
        return self.request.user.is_staff

    model = Composition


class CompositionAdd(PermissionRequiredMixin, View):
    """Allows cretion of new composition"""
    permission_required = 'c_can_add_composition'
    def get(self, request, *args, **kwargs):
        context = {
            'field_form': FieldForm(),
            'compose_form': ComposeForm()
        }
        return render(request, 'staff_only/compose.html', context)

    def post(self, request, *args, **kwargs):
        field_form = FieldForm(request.POST)
        compose_form = ComposeForm(request.POST)
        context = {
            'field_form': field_form,
            'compose_form': compose_form
        }

        if field_form.is_valid() and compose_form.is_valid():
            field_set = field_form.cleaned_data['field_set']
            name = compose_form.cleaned_data['name']
            instruction = compose_form.cleaned_data['instruction']
            field_set = ', '.join(field_set)
            composition = Composition.objects.create(name=name, instruction=instruction, field_set=field_set)
            return redirect(reverse('staff_only:compositions'))
        return render(request, 'staff_only/compose.html', context)


class CompositionDetailView(UserPassesTestMixin, DetailView):
    """Displays detailed information about composition"""
    def test_func(self):
        return self.request.user.is_staff

    model = Composition


class CompositionEditView(PermissionRequiredMixin, View):
    """Allows modification of composition"""
    permission_required = 'c_can_modify_composition'
    def get(self, request, *args, **kwargs):
        composition = get_object_or_404(Composition, pk=kwargs['pk'])
        composition.field_set.split(', ')
        context = {
            'field_form': FieldForm(initial={'field_set': composition.field_set.split(', ')}),
            'compose_form': ComposeForm(instance=composition)
        }
        return render(request, 'staff_only/compose.html', context)

    def post(self, request, *args, **kwargs):
        composition = get_object_or_404(Composition, pk=kwargs['pk'])
        field_form = FieldForm(request.POST)
        compose_form = ComposeForm(request.POST)
        context = {
            'field_form': field_form,
            'compose_form': compose_form
        }

        if field_form.is_valid() and compose_form.is_valid():
            composition.name = compose_form.cleaned_data['name']
            composition.instruction = compose_form.cleaned_data['instruction']
            composition.field_set = ', '.join(field_form.cleaned_data['field_set'])
            composition.save()
            return redirect(reverse('staff_only:compositions'))
        return render(request, 'staff_only/compose.html', context)


class CompositionDeleteView(PermissionRequiredMixin, DeleteView):
    """Allows delete composition."""
    permission_requred = 'c_can_modify_composition'
    model = Composition
    success_url = reverse_lazy('staff_only:compositions')




class AscriptionAddView(PermissionRequiredMixin, View):
    """Enables ascription of existing Composition to a client."""
    permission_required = 'c_can_toggle_ascription'
    def get(self, request, *args, **kwargs):
        context = {
            'form': AscriptionForm(),
        }
        return render(request, 'staff_only/ascription_form.html', context)
        form = AscriptionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            for composition in form.cleaned_data['composition']:
                Ascription.objects.create(user=user, composition=composition)
        return render(request, 'staff_only/ascription_form.html')


class ClientAscriptionView(UserPassesTestMixin, View):
    """User's detail page with list of all existing compositions"""
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        ascriptions = Ascription.objects.filter(user=user, active=True)
        ascr = [x.composition.pk for x in ascriptions]
        compositions = Composition.objects.all()
        context = {
            'user': user,
            'ascr': ascr,
            'compositions': compositions
        }
        return render(request, 'staff_only/client_ascription.html', context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        composition = get_object_or_404(Composition, pk=request.POST.get('composition'))
        return redirect(reverse('staff_only:toggle_ascription', kwargs={'user_pk': user.pk, 'comp_pk': composition.pk}))


class ToggleAscriptionView(PermissionRequiredMixin, View):
    """Enables switching on and off client's ascription to an exercise"""
    permission_required = 'c_can_toggle_ascritpion'
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_pk'])
        composition = get_object_or_404(Composition, pk=kwargs['comp_pk'])
        try:
            ascription = Ascription.objects.get(composition=composition, user=user)
            if ascription.active == False:
                ascription.active = True
            else:
                ascription.active = False
            ascription.save()
        except Ascription.DoesNotExist:
            ascription = Ascription.objects.create(composition=composition, user=user)
        return redirect(reverse('staff_only:client_ascriptions', kwargs={'pk': user.pk}))


class ManageAscriptionsView(PermissionRequiredMixin, View):
    """Allows add or strip ascription of a particular composition to all of clients"""
    permission_required = 'c_can_toggle_ascription'
    def get(self, request, *args, **kwargs):
        composition = get_object_or_404(Composition, pk=kwargs['pk'])
        ascriptions = Ascription.objects.filter(composition=composition, active=True)
        for ascription in ascriptions:
            print(ascription, ascription.active)
        usr = [x.user.pk for x in ascriptions]
        print(f'manage ascriptions usr: {usr}')
        users = User.objects.filter(is_staff=False)

        context = {
            'composition': composition,
            'usr': usr,
            'users': users,
        }
        print(context)
        return render(request, 'staff_only/manage_ascription.html', context)

    def post(self, request, *args, **kwargs):
        composition = get_object_or_404(Composition, pk=kwargs['pk'])
        old_usr = set([str(x.user.pk) for x in composition.ascription_set.filter(active=True)])
        new_usr = set(request.POST.getlist('users'))
        add = new_usr.difference(old_usr)
        strip = old_usr.difference(new_usr)
        for u in add:
            try:
                ascription = Ascription.objects.get(composition=composition, user_id=int(u))
                ascription.active = True
                ascription.save()
            except Ascription.DoesNotExist:
                Ascription.objects.create(composition=composition, user_id=int(u))
            else:
                ascription.active = True
                ascription.save()
        for u in strip:
            ascription = Ascription.objects.get(composition=composition, user_id=int(u))
            ascription.active = False
            ascription.save()
        return redirect(reverse('staff_only:compositions'))
