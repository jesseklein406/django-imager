from __future__ import absolute_import

from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from .models import ImagerProfile


class ImagerProfileDetailView(LoginRequiredMixin, DetailView):
    model = ImagerProfile
    template_name = "imager_profile/profile_detail.html"
        
