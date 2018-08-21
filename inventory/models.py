from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nick_name = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()


class Book(models.Model):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
