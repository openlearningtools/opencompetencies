from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from competencies.models import *


# --- School admin, with inline subjects ---
class SubjectAreaInline(admin.TabularInline):
    model = SubjectArea
    extra = 1

class SchoolAdmin(admin.ModelAdmin):
    inlines = [SubjectAreaInline]

# --- Subject Area admin, with subdisciplines inline
class SubdisciplineAreaInline(admin.TabularInline):
    model = SubdisciplineArea
    extra = 1

class SubjectAreaAdmin(admin.ModelAdmin):
    inlines = [SubdisciplineAreaInline]

# --- Subdiscipline Area admin, with competency areas inline
class GraduationStandardInline(admin.TabularInline):
    model = GraduationStandard
    extra = 1

class SubdisciplineAreaAdmin(admin.ModelAdmin):
    inlines = [GraduationStandardInline]

# --- Competency Area admin, with performance indicators inline
class PerformanceIndicatorInline(admin.TabularInline):
    model = PerformanceIndicator
    extra = 1

class GraduationStandardAdmin(admin.ModelAdmin):
    inlines = [PerformanceIndicatorInline]

# --- Performance Indicator admin, with learning objectives inline
class LearningObjectiveInline(admin.TabularInline):
    model = LearningObjective
    extra = 1

class PerformanceIndicatorAdmin(admin.ModelAdmin):
    inlines = [LearningObjectiveInline]

# --- Pathway Admin ---
class PathwayAdmin(admin.ModelAdmin):
    pass

# --- User Admin ---
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.register(School, SchoolAdmin)
admin.site.register(SubjectArea, SubjectAreaAdmin)
admin.site.register(SubdisciplineArea, SubdisciplineAreaAdmin)
admin.site.register(GraduationStandard, GraduationStandardAdmin)
admin.site.register(PerformanceIndicator, PerformanceIndicatorAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
