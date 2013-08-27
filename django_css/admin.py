from django.contrib import admin

from django_css.models import *


# --- ELAElement admin, with inline everything ---
class InitiativeInline(admin.TabularInline):
    model = Initiative

class FrameworkInline(admin.TabularInline):
    model = Framework

class DomainInline(admin.TabularInline):
    model = Domain

class GradeInline(admin.TabularInline):
    model = Grade

class StandardInline(admin.TabularInline):
    model = Standard

class ComponentInline(admin.TabularInline):
    model = Component

class ELAElementAdmin(admin.ModelAdmin):
    inlines = [InitiativeInline, FrameworkInline, DomainInline, 
               GradeInline, StandardInline, ComponentInline]


admin.site.register(ELAElement, ELAElementAdmin)
