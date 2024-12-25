from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Consumer

class ConsumerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name','gender', 'age')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name','gender', 'age')}),
    )

admin.site.register(Consumer, ConsumerAdmin)
