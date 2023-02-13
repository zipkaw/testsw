from django.views.generic.edit import FormMixin
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect

class DeleteToTrashMixin(BaseDetailView, FormMixin):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete' in request.POST:
            self.object.deleted = True
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
             