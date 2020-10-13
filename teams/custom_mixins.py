from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect

class FullProfileOrStaffMixin(object):
   
    def dispatch(self, request, *args, **kwargs):
        print('Full profile: running dispatch')
        if not (self.request.user.has_full_profile or self.request.user.is_staff):
            print('Full profile: dispatch redirect')
            return redirect('teams:profile_info')
        print('Full profile: dispatch passed')
        return super(FullProfileOrStaffMixin, self).dispatch(
            request, *args, **kwargs)



class SameUserOnlyMixin(object):

    def has_permissions(self):
        print('Same user: running has_permissions')
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            print('Same user: dispatch failed')
            raise Http404('Page not found.')
        print('Same user: dispatch passed')
        return super(SameUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)


class SameUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        print(f'authenticated: {request.user.is_authenticated}')
        print(f'authenticated: {request.user == self.get_object()}')
        if not (request.user.is_authenticated and request.user == self.get_object()):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



class StaffOnlyMixin(AccessMixin):
    """Verify that the current user is staff."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404('Page not found.')
        return super().dispatch(request, *args, **kwargs)