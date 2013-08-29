from django.contrib import admin

from django_ccss.models import *


class InitiativeAdmin(admin.ModelAdmin):
    model = Initiative

class FrameworkAdmin(admin.ModelAdmin):
    model = Framework

class DomainAdmin(admin.ModelAdmin):
    model = Domain

class GradeAdmin(admin.ModelAdmin):
    model = Grade

class StandardAdmin(admin.ModelAdmin):
    model = Standard

class ComponentAdmin(admin.ModelAdmin):
    model = Component

class ELAElementAdmin(admin.ModelAdmin):
    model = ELAElement

admin.site.register(Initiative)
admin.site.register(Framework)
admin.site.register(Domain)
admin.site.register(Grade)
admin.site.register(Standard)
admin.site.register(Component)
admin.site.register(ELAElement)
