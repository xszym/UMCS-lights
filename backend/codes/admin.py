from django.contrib import admin
from .models import Code, CustomUser


admin.site.register(CustomUser)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'approved', 'author', 'date', 'is_example'
    )
