from django.contrib import admin

from .models import (
    Shareholder,
    Security,
    Investor,
    Addition,
    Certificate)


class ShareholderInline(admin.TabularInline):
    model = Shareholder
    extra = 0


class AdditionInline(admin.TabularInline):
    model = Addition
    fieldsets = [
        (None, {
            'fields': ['date', 'authorized', 'notes'],
            'description': "The additional shares/options authorized\
            for this class of security."
            },
        ),
    ]
    extra = 0


class InvestorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ['shareholder__certificate__security']
    ordering = ['name']
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = [
        (None, {
            'fields': ['name', 'slug',],
            'description': "Investor represents the entity making the \
            decision to invest.  Examples of investors are VC firms, \
            angels, banks, note holders, friends, family and fools. \
            Investors differ from shareholders in that shareholders, \
            listed inline below, represent the legal entity making \
            the investment.  VCs and other professional investors \
            will often split their stake among funds in their portfolio\
            (such as Entrepreneur's Fund VIII, Principal's Fund III, etc.)\
            For Angels or other individual investors, this could also simply\
            be an instrument like a family Trust, or other legal entity\
            other than the name of the investor.  The best way to handle\
            these details is the keep a single name for the investor to\
            which you'd normally refer to them, and the legal/multiple\
            entities as shareholders.  These shareholders will be the\
            actual holders of each certificate of shares/options.  Also\
            be aware that since the shareholders legally hold the certificates\
            there must always be at least one shareholder, which can be the same\
            name as the investor if you so desire."
            }
        ),
        ('Contact Information', {
            'fields': ['contact', 'address', ('city', 'state', 'zipcode',)],
            'classes': ['collapse'],
            'description': "Contact details for the investor and \
            related shareholders."
            }
        ),
        ('Notes', {
            'fields': ['notes'],
            'classes': ['collapse'],
            'description': "Notes related to the investor."
            }
        )
    ]
    inlines = [ShareholderInline]


class SecurityAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'date', 'name', 'security_type', 'pre','seniority')
    list_filter = ['security_type']
    ordering = ['date']
    fieldsets = [
        (None, {
            'fields': ['name', 'slug', 'date', 'security_type', 'price_per_share', 'pre', 'conversion_ratio', 'liquidation_preference', 'seniority'],
            'description': "A Security represents a specific financing \
            instrument, and is usually accompanied by its own form of \
            legal documentation.  Examples of securities include common \
            stock, a Series A offering, a covertible loan, etc.  \
            Securities can be similiar but have different terms, \
            such as a Series A offering and a Series B offering, \
            both of whichare preferred stock but may have different \
            prices or preferences."
            }
        ),
        ('Preferred Participation', {
            'fields': ['is_participating', 'participation_cap'],
            'classes':['collapse'],
            'description': "Some details typically associated only with preferred stock."
            }
        ),
        ('Convertible Specifics', {
            'fields': ['price_cap', 'discount_rate', 'interest_rate',],
            'classes':['collapse'],
            'description': 'Some details typically associated only with convertible debt.'
            }
        ),
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

admin.site.register(Security, SecurityAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(Certificate, CertificateAdmin)
