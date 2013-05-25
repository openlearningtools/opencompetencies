from django.contrib import admin

from competencies.models import *


# --- School admin, with inline subjects ---
class SubjectAreaInline(admin.TabularInline):
    model = SubjectArea
    extra = 1

class PathwayInline(admin.TabularInline):
    model = Pathway
    extra = 1

class SchoolAdmin(admin.ModelAdmin):
    inlines = [SubjectAreaInline, PathwayInline]

# --- Subject Area admin, with subdisciplines inline
class SubdisciplineAreaInline(admin.TabularInline):
    model = SubdisciplineArea
    extra = 1

class SubjectAreaAdmin(admin.ModelAdmin):
    inlines = [SubdisciplineAreaInline]

# --- Subdiscipline Area admin, with competency areas inline
class CompetencyAreaInline(admin.TabularInline):
    model = CompetencyArea
    extra = 1

class SubdisciplineAreaAdmin(admin.ModelAdmin):
    inlines = [CompetencyAreaInline]

# --- Competency Area admin, with essential understandings inline
class EssentialUnderstandingInline(admin.TabularInline):
    model = EssentialUnderstanding
    extra = 1

class LevelInline(admin.TabularInline):
    model = Level
    extra = 1

class CompetencyAreaAdmin(admin.ModelAdmin):
    inlines = [EssentialUnderstandingInline, LevelInline]

# --- Essential Understanding admin, with learning targets inline
class LearningTargetInline(admin.TabularInline):
    model = LearningTarget
    extra = 1

class EssentialUnderstandingAdmin(admin.ModelAdmin):
    inlines = [LearningTargetInline]

# --- Pathway Admin ---
class PathwayAdmin(admin.ModelAdmin):
    pass


admin.site.register(School, SchoolAdmin)
admin.site.register(SubjectArea, SubjectAreaAdmin)
admin.site.register(SubdisciplineArea, SubdisciplineAreaAdmin)
admin.site.register(CompetencyArea, CompetencyAreaAdmin)
admin.site.register(EssentialUnderstanding, EssentialUnderstandingAdmin)
admin.site.register(Pathway, PathwayAdmin)
