from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PrivateUser, PublicUser, UserInterests

class PrivateUserAdmin(UserAdmin):
       fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ()}), 
    )
       add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ()}), 
        )
       
@admin.register(PublicUser, UserInterests)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

admin.site.register(PrivateUser, PrivateUserAdmin)

# Register your models here.
