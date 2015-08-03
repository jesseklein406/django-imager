from __future__ import absolute_import

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from .forms import ProfileUpdateForm, UserUpdateForm
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


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile
        )
        user_form = UserUpdateForm(
            request.POST, instance=request.user
        )
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return HttpResponseRedirect(reverse('profile:detail'))
        else:
            context = {
                'profile_form': profile_form.as_p, 'user_form': user_form.as_p
            }
            return render(
                request, 'imager_profile/profile_edit.html', context
            )
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
        context = {
            'profile_form': profile_form.as_p, 'user_form': user_form.as_p
        }
        return render(
            request, 'imager_profile/profile_edit.html', context
        )
