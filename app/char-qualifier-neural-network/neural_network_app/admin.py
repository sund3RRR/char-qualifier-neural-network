from django.contrib import admin

from .models import ImageModel

@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'char']
    list_filter = ('char',)