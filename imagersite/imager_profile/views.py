from __future__ import absolute_import

from django.views.generic import DetailView, UpdateView
from braces.views import LoginRequiredMixin

from .models import ImagerProfile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = ImagerProfile
    template_name = "imager_profile/profile_detail.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ImagerProfile
    fields = ['camera', 'address', 'web_url', 'type_photography']

    def get_object(self):
        return self.request.user
