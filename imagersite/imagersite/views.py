from django.views.generic.base import TemplateView
from django.shortcuts import render

from imager_images.models import Photo


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        main_photo = Photo.objects.filter(
            published='public').order_by('?').first()
        context['photo'] = main_photo
        return context
