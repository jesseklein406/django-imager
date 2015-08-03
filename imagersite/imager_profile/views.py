from __future__ import absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView
from braces.views import LoginRequiredMixin

from .models import ImagerProfile


class ProfileActionMixin(object):

    fields = ['camera', 'address', 'web_url', 'type_photography']

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ProfileActionMixin, self).form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = ImagerProfile
    template_name = "imager_profile/profile_detail.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ImagerProfile
    fields = ['camera', 'address', 'web_url', 'type_photography']
    template_name_suffix = '_update_form'
