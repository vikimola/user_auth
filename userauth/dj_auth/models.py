import uuid

from django.db import models


# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, default=uuid.uuid1)
