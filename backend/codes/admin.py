from django.contrib import admin
from .models import Code, CustomUser, Config


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
