from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse

from blog.settings import AUTH_USER_MODEL


class Trader(AbstractUser):
    city = models.CharField(max_length=255)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.username}({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("marketplace:trader-detail", kwargs={'pk': self.pk})


class Publication(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publications"
    )
    text = models.TextField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    image = models.ImageField(upload_to="product_images/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse("blog:product-detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name}"
