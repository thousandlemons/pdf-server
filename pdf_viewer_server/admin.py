from abc import abstractmethod

from django.contrib import admin
from django.core.exceptions import PermissionDenied


class ObjectLevelPermissionAdmin(admin.ModelAdmin):
    """ModelAdmin with object-level permission control.

    By default, anyone can create, and superusers can do whatever they want.

    Then, for normal users, they can delete or change if and only if self.has_permission(),
    an abstract method to be implemented by child classes, returns True.

    Attributes:
        superuser_only_fields: (optional) a list of attributes only visible to superusers
        superuser_only_actions: (optional) a list of actions only visible to superusers

    """

    class Media:
        css = None
        js = None

    superuser_only_fields = []
    superuser_only_actions = []

    @abstractmethod
    def has_permission(self, request, obj):
        """This method is only useful when request.user is not a superuser

        Returns:
            True or False, meaning if the permission is granted

        """
        pass

    def show_save_buttons(self, option):
        """If option is False, add static css/js to hide <div class="submit-row"></div>

        """
        if option:
            ObjectLevelPermissionAdmin.Media.css = None
            ObjectLevelPermissionAdmin.Media.js = None
        else:
            ObjectLevelPermissionAdmin.Media.css = {'all': ('css/hide-save-row.css',)}
            ObjectLevelPermissionAdmin.Media.js = ('js/hide-save.row.js',)

    def get_superuser_only_fields(self):
        """Convert self.superuser_only_fields to list and return

        """
        return list(self.superuser_only_fields)

    def is_superuser(self, request):
        """Returns True if the user in the request is a superuser

        """
        return request.user.is_superuser

    def get_fields(self, request, obj=None):
        """Override. Remove self.superuser_only_fields from super().get_fields()

        """
        fields = super(ObjectLevelPermissionAdmin, self).get_fields(request, obj)
        if not self.is_superuser(request):
            for field in self.get_superuser_only_fields():
                if field in fields:
                    fields.remove(field)
        return fields

    def get_readonly_fields(self, request, obj=None):
        """Override. Mark all fields as read-only if no delete permission (creator/superuser)

        """
        if self.is_superuser(request) or self.has_delete_permission(request, obj):
            return self.readonly_fields

        return [f.name for f in self.model._meta.fields]

    def has_delete_permission(self, request, obj=None):
        """Override. Return True if request.user is the owner of obj, or a superuser
        """
        if obj is None:
            return True
        if self.is_superuser(request):
            return True
        return self.has_permission(request, obj)

    def save_model(self, request, obj, form, change):
        """Override. Check has_delete_permission() before saving a model.

        If the object is newly created (marked by "change" flag being False), return true.
        No need to check has_add_permission() here because it has been checked by super()

        Raises:
            PermissionDenied: if has_delete_permission() fails

        """
        if not change or self.has_delete_permission(request, obj):
            super(ObjectLevelPermissionAdmin, self).save_model(request, obj, form, change)
        else:
            raise PermissionDenied

    def get_form(self, request, obj=None, **kwargs):
        """Override. Hide save buttons if self.has_delete_permission() fails.

        """
        self.show_save_buttons(self.has_delete_permission(request, obj))
        return super(ObjectLevelPermissionAdmin, self).get_form(request, obj, **kwargs)

    def get_actions(self, request):
        """Override. Hide superuser_only_actions if request.user is not a superuser.

        """
        actions = super(ObjectLevelPermissionAdmin, self).get_actions(request)
        if self.is_superuser(request):
            return super(ObjectLevelPermissionAdmin, self).get_actions(request)
        else:
            del actions['delete_selected']
            for action in self.superuser_only_actions:
                del actions[action.__name__]
            return actions


class OwnerAndSuperuserOnlyAdmin(ObjectLevelPermissionAdmin):
    """Object level permission: only superuser and owners can delete/modify; anyone can create

    """
    def has_permission(self, request, obj):
        """To use this Admin class, the model class must implement is_owned_by()

        """
        return obj.is_owned_by(request.user)


class SuperuserOnlyAdmin(OwnerAndSuperuserOnlyAdmin):
    """Object level permission: non-superusers can view only.

    It only restricts has_add_permission() and has_delete_permission() to superusers, and
    other methods in OwnerAndSuperuserOnlyAdmin class will do the job to prevent non-superusers
    from making changes or create objects.

    This is a compromise because by default if has_change_permission() is False, the user
    cannot even see the model detail page, or even the model in the model list. We want the user
    to see the some of the model details but not modifying or creating models.

    """

    def has_add_permission(self, request):
        return self.is_superuser(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_superuser(request)
