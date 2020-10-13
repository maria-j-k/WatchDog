from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, View

from .forms import AscribeCompositionForm, AscriptionForm, ComposeForm, FieldForm
from .models import Ascription, Composition
from teams.models import User


class ClientListView(ListView):
    model = User
    template_name ='staff_only/user_list.html'
    queryset = User.objects.filter(is_staff=False)


class ClientDetailView(DetailView):
    model = User
    template_name ='staff_only/user_detail.html'




class CompositionListView(ListView):
    model = Composition


class CompositionAdd(View):
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
    model = Composition


class CompositionEditView(View):
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
    model = Composition
    success_url = reverse_lazy('staff_only:compositions')




class AscriptionListView(ListView):
    model = Ascription
    ordering = 'composition'


class AscriptionDetailView(DetailView):
    model = Ascription


class AscriptionAddView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AscriptionForm(),
        }
        return render(request, 'staff_only/ascription_form.html', context)

    def post(self, request, *args, **kwargs):
        form = AscriptionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            for composition in form.cleaned_data['composition']:
                Ascription.objects.create(user=user, composition=composition)
        return render(request, 'staff_only/ascription_form.html')


class ClientAscriptionView(View):
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









