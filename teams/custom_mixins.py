from django.http import Http404
from django.shortcuts import redirect

class FullProfileOnlyMixin(object):

    def has_permissions(self):
        print('running has_permissions')
        return self.get_object().has_full_profile
      
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return redirect('teams:profile_info')
        return super(FullProfileOnlyMixin, self).dispatch(
            request, *args, **kwargs)



class SameUserOnlyMixin(object):

    def has_permissions(self):
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(SameUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)
