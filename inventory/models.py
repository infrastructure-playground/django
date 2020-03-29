import time
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nick_name = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='icons', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id',]


# @receiver(post_save, sender=Book)
# def book_follow_up(sender, instance, created, **kwargs):
#     if created:
#         with transaction.atomic():
#             author_inst = Author.objects.select_for_update().first()
#             author_inst.save()
#             instance.save()
#     # with transaction.atomic():
#     #     print('timer starts')
#     #     # time.sleep(10)
#     #     print('timer ends')
#     #     return
#
#
# def claim_something(book):
#     with transaction.atomic():
#         author_inst = Author.objects.select_for_update().first()
#         author_inst.save()