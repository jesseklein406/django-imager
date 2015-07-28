from django.views.generic.base import TemplateView
from django.shortcuts import render


# def index(request):
#     context = {'name': 'bob'}
#     return render(request, 'index.html', context)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['photo'] = 'images/django_1024x768.png'
        return context
