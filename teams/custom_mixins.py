from django.http import Http404
from django.shortcuts import redirect

class FullProfileOnlyMixin(object):

    # def has_permissions(self):
    #     print('Full profile: running has_permissions')
    #     return self.request.user.has_full_profile
      
    def dispatch(self, request, *args, **kwargs):
        print('Full profile: running dispatch')
        if not self.request.user.has_full_profile:
            print('Full profile: dispatch redirect')
            return redirect('teams:profile_info')
        print('Full profile: dispatch passed')
        return super(FullProfileOnlyMixin, self).dispatch(
            request, *args, **kwargs)



class SameUserOnlyMixin(object):

    def has_permissions(self):
        print('Same user: running has_permissions')
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            print('Same user: dispatch failed')
            raise Http404('You do not have permission.')
        print('Same user: dispatch passed')
        return super(SameUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)


# class ProductExistsRequiredMixin:

#     def dispatch(self, request, *args, **kwargs):
#         if Product.objects.filter(pk=1, activate=True):
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied