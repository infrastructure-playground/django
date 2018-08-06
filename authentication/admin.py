from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_full_name')


# Register your models here.
admin.site.register(Account, AccountAdmin)
