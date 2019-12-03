from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from UserApp.models import Account


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ['email', 'username', 'is_admin', 'is_staff']
    search_fields = ('email', 'username')
    # readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)