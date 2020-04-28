import os
import random
from django.db import models
from django.urls import reverse
from django.db.models import Q
from tags.models import Tags


def get_filename_ext(filepath):
    filename = os.path.basename(filepath)
    filelocation, fil_ext = os.path.splitext(filename)
    return filelocation, fil_ext


def upload_path(instance, filename):

    newfilename = random.randint(100, 25468799)
    filename, ext = get_filename_ext(filename)
    finalFilename = f"{newfilename}{ext}"
    return f"products/images/{finalFilename}"


class ProductQuerySet(models.QuerySet):
    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        """ calling ProductQuerset """
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to=upload_path)
    slug = models.SlugField(blank=True, null=True)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)

    objects = ProductManager()

    def __str__(self):
        return self.title+str(self.id)

    def get_absolute_url(self):
        # return f"/product/{self.slug}"
        return reverse("product:details", kwargs={"slug": self.slug})

    @property
    def name(self):
        return self.title
