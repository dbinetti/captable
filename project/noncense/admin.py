from django.contrib import admin

from .models import MobileUser

from captable.models import Company


class CompanyInline(admin.TabularInline):
    model = Company.owner.through


class MobileUserAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [CompanyInline]


admin.site.register(MobileUser, MobileUserAdmin)
