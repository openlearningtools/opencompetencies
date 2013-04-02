from competencies.models import SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget
from django.contrib import admin

class SubdisciplineAreaInline(admin.TabularInline):
    model = SubdisciplineArea
    extra = 1

class SubjectAreaAdmin(admin.ModelAdmin):
    inlines = [SubdisciplineAreaInline]


admin.site.register(SubjectArea, SubjectAreaAdmin)
