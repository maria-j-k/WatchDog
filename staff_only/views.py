from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (DeleteView, DetailView, ListView, UpdateView,
        View)

from .forms import (AscribeCompositionForm, AscriptionForm, ComposeForm,
FieldForm, MakeStaffForm)
from .models import Ascription, Composition
from teams.models import User


class StaffListView(ListView):
    """Displays all staff members who has not admin status."""
    model = User
    template_name = 'staff_only/staff_list.html'
    queryset = User.objects.filter(is_staff=True, is_superuser=False)


class MakeStaff(View):
    """Allows to change the status of a user and accord staff privileges."""
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


class ClientListTraining(ListView):
    """Displays list of clients who has already exercises ascribed."""
    model = User
    template_name = 'staff_only/training_list.html'
    queryset = User.objects.filter(ascription__isnull=False, is_active=True).distinct()



class ClientsNeedAscription(ListView):
    """Displays all active users with full profile, who has no exercises
    ascribed yet or whose ascriptions has been anulated."""
    model = User
    template_name = 'staff_only/need_ascription.html'
    queryset = User.objects.filter(_has_full_profile=True,
                                   ascription__isnull=True,
                                   is_staff=False)


class RegisteredPersons(ListView):
    """Displays all person, who has created an account, but didn't fill out their
    profile."""
    model = User
    template_name = 'staff_only/registered_persons.html'
    queryset = User.objects.filter(_has_full_profile=False, is_staff=False)


class SuspendedClients(ListView):
    """Displays all clients who has been suspended but not deleted"""
    model = User
    template_name = 'staff_only/suspended_clients.html'
    queryset = User.objects.filter(is_active=False)




class ClientDetailView(DetailView):
    """Displays detailed information about a client."""
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


class CompositionListView(ListView):
    """Displays list of all compositions with the names of clients, if the composition is ascribed to any client.
    """
    model = Composition


class CompositionAdd(View):
    """Allows cretion of new composition"""
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


class CompositionDetailView(DetailView):
    """Displays detailed information about composition"""
    model = Composition


class CompositionEditView(View):
    """Allows modification of composition"""
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


class CompositionDeleteView(DeleteView):
    """Allows delete composition."""
    model = Composition
    success_url = reverse_lazy('staff_only:compositions')




class AscriptionAddView(View):
    """Enables ascription of existing Composition to a client."""
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


class ClientAscriptionView(View):
    """User's detail page with list of all existing compositions, allows
    strp or add ascription to an exercise to given client."""
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
        try:
            ascription = Ascription.objects.get(composition=composition, user=user)
            if ascription.active == False:
                ascription.active = True
            else:
                ascription.active = False
            ascription.save()
        except Ascription.DoesNotExist:
            ascription = Ascription.objects.create(composition=composition, user=user)
        compositions = Composition.objects.all()
        ascriptions = Ascription.objects.filter(user=user, active=True)
        ascr = [x.composition.pk for x in ascriptions]
        context = {
            'user': user,
            'ascr': ascr,
            'compositions': compositions
        }
        return render(request, 'staff_only/client_ascription.html', context)



class ManageAscriptionsView(View):
    """Allows add or strip ascription of a particular composition to all of clients"""
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
