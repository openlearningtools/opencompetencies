from django.contrib import admin

from django_ccss.models import *


class InitiativeAdmin(admin.ModelAdmin):
    model = Initiative

class FrameworkAdmin(admin.ModelAdmin):
    model = Framework

class DomainAdmin(admin.ModelAdmin):
    model = Domain


admin.site.register(Initiative)
admin.site.register(Framework)
admin.site.register(Domain)
