from django.contrib import admin

from .models import LessonStatistic, Profile, ModuleTradeInfo

NUMBER_OF_EXTRA_FORMS = 1


class LessonStatisticInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = LessonStatistic
    autocomplete_fields = ("lesson",)


class ModuleTradeInline(admin.TabularInline):
    extra = NUMBER_OF_EXTRA_FORMS
    model = ModuleTradeInfo
    autocomplete_fields = ("module",)


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'purchased_modules',
    ]
    inlines = [
        LessonStatisticInline,
        ModuleTradeInline,
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(LessonStatistic)
admin.site.register(ModuleTradeInfo)
