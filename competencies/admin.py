from competencies.models import SubjectArea, SubdisciplineArea, CompetencyArea, EssentialUnderstanding, LearningTarget
from django.contrib import admin

class SubdisciplineAreaInline(admin.TabularInline):
    model = SubdisciplineArea
    extra = 1

class SubjectAreaAdmin(admin.ModelAdmin):
    inlines = [SubdisciplineAreaInline]


class EssentialUnderstandingInline(admin.TabularInline):
    model = EssentialUnderstanding
    extra = 1

class CompetencyAreaAdmin(admin.ModelAdmin):
    inlines = [EssentialUnderstandingInline]


class LearningTargetInline(admin.TabularInline):
    model = LearningTarget
    extra = 1

class EssentialUnderstandingAdmin(admin.ModelAdmin):
    inlines = [LearningTargetInline]

admin.site.register(SubjectArea, SubjectAreaAdmin)
admin.site.register(CompetencyArea, CompetencyAreaAdmin)
admin.site.register(EssentialUnderstanding, EssentialUnderstandingAdmin)
