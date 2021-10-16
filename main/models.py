from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, null=True, related_name='reviews',  blank=True, on_delete=models.CASCADE)


class ConfirmCode(models.Model):
    code = models.CharField(max_length=100)
    valid_until = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
