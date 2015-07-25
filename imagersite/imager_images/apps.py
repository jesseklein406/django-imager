from django.apps import AppConfig


class ImagerProfileConfig(AppConfig):
    name = 'imager_images'
    verbose_name = 'Imager images'

    def ready(self):
        import imager_images.signals
