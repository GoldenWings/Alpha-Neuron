from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Trainer


class TrainerInline(admin.StackedInline):
    model = Trainer
    can_delete = False
    verbose_name_plural = 'trainer'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (TrainerInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'picture', 'role']
    list_select_related = ('trainer',)

    def picture(self, instance):
        return instance.trainer.picture

    def role(self, instance):
        return instance.trainer.role

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
