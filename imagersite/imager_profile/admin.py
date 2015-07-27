from django.contrib import admin
from .models import ImagerProfile


class CategoryUser(admin.ModelAdmin):
    list_display = ['email', 'user_id']

    class Meta:
        model = ImagerProfile

admin.site.register(ImagerProfile)
        
