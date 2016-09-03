from django.contrib import admin

from version.models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_by', 'timestamp')
    readonly_fields = ('created_by', 'timestamp')
