from django.db import models

# Create your models here.

class ImageModel(models.Model):
    image = models.ImageField("Image", upload_to='images/')
    char = models.CharField("Char", max_length=1)