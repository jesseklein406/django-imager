from django.views.generic.base import TemplateView

from imager_images.models import Photo


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        default_photo = 'static/images/django_1024x768.png'
        random = Photo.objects.filter(
            published='public').order_by('?').first()
        context['photo'] = random.photo.url if random else default_photo
        return context
