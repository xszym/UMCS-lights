from django.contrib import admin
from .models import Code, CustomUser, Config, AnimationPriorityQueueElement


admin.site.register(CustomUser)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'approved', 'author', 'date', 'is_example'
    )

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        'force_stop', 'force_run'
    )

@admin.register(AnimationPriorityQueueElement)
class AnimationPriorityQueueElementAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'priority'
    )
