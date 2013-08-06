from django.contrib import admin

from .models import (
    Shareholder,
    Security,
    Transaction,
    Investor,
    Addition,
    Certificate)


class CertificateInline(admin.TabularInline):
    model = Certificate
    fields = ('granted', 'exercised', 'cancelled')


class ShareholderInline(admin.TabularInline):
    model = Shareholder


class TransactionInline(admin.TabularInline):
    model = Transaction
    exclude = ('notes',)


class AdditionInline(admin.TabularInline):
    model = Addition
    exclude = ('notes',)


class InvestorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name']
    ordering = ['name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ShareholderInline]


class ShareholderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class SecurityAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'date', 'name', 'security_type', 'price_cap',
        'discount_rate', 'interest_rate', 'pre')
    ordering = ['date']
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'date', 'security_type']}),
        ('Preferred', {'fields': ['price_per_share', 'pre', 'conversion_ratio', 'liquidation_preference', 'seniority', 'is_participating', 'participation_cap'], 'classes':['collapse']}),
        ('Debt', {'fields': ['price_cap', 'discount_rate', 'interest_rate', 'default_conversion_price', 'conversion_security'], 'classes':['collapse']}),
    ]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AdditionInline]


class CertificateAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        '__unicode__', 'shares', 'returned', 'cash', 'refunded',
        'principal', 'forgiven', 'granted', 'exercised', 'cancelled']
    ordering = ['name']
    list_filter = ['security__security_type']

admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(Transaction)
admin.site.register(Addition)
admin.site.register(Certificate, CertificateAdmin)
