from django.contrib import admin

from version.models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'timestamp')
    readonly_fields = ('owner', 'timestamp')
