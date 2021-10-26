from django.contrib import admin
from .models import (Lesson, Section, Module, Course, Categorie, Rating,
                     Feature, Study, Filling, TargetAudience, GetToKnow,
                     ExchangeRate)


NUMBER_OF_EXTRA_FORMS = 1


class CourseFeatureInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Feature.courses.through


class CourseStudyInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Study.courses.through


class CourseFillingInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Filling.courses.through


class CourseAudienceInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = TargetAudience.courses.through


class CourseToKnowInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = GetToKnow.courses.through


class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ['updated', 'timestamp']
    inlines = [
        CourseFeatureInline,
        CourseStudyInline,
        CourseFillingInline,
        CourseAudienceInline,
        CourseToKnowInline,
    ]


class ModuleFeatureInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Feature.modules.through


class ModuleStudyInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Study.modules.through
    verbose_name = 'Что выучишь в модуле'


class ModuleSectionInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Section


class ModuleAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    inlines = [
        ModuleFeatureInline,
        ModuleStudyInline,
        ModuleSectionInline
    ]
    search_fields = ("name",)


class SectionLessonInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = Lesson


class SectionAdmin(admin.ModelAdmin):
    inlines = [SectionLessonInline]


class ExchangeAdmin(admin.ModelAdmin):
    readonly_fields = ['updated']


class LessonAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_select_related = ("section__module",)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Rating)
admin.site.register(Categorie)
admin.site.register(Section, SectionAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Feature)
admin.site.register(Study)
admin.site.register(Filling)
admin.site.register(TargetAudience)
admin.site.register(GetToKnow)
admin.site.register(ExchangeRate, ExchangeAdmin)
