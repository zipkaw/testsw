from django.views.generic.edit import FormMixin
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect


class DeleteCardToTrashMixin(BaseDetailView, FormMixin):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete' in request.POST:
            self.object.deleted = True
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())


class TrashOptionsMixin(BaseDetailView): 
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete-permanently' in request.POST:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        if 'restore' in request.POST:
            self.object.deleted = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
