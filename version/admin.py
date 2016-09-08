from django.contrib import admin

from pdf_server.admin import OwnerAndSuperuserOnlyAdmin
from version.models import Version


@admin.register(Version)
class VersionAdmin(OwnerAndSuperuserOnlyAdmin):
    model_class = Version

    list_display = ('name', 'id', 'owner', 'timestamp')
    readonly_fields = ('owner', 'timestamp')

    list_filter = ('owner',)

    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        # change = not add
        # in the case of creating a new version, change == False
        if not change:
            obj.owner = request.user
            obj.save()
        else:
            super(VersionAdmin, self).save_model(request, obj, form, change)
