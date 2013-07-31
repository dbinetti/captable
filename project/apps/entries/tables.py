import django_tables2 as tables
from django_tables2.utils import A

# from templatetags.captabletags import percentage, shares, currency, price

from .models import (
    Shareholder,
    Security,
    Certificate,
    Investor,
)

class RataColumn(tables.Column):
    def render(self, value):
        if value:
            return percentage(value)
        else:
            return '-'


class SharesColumn(tables.Column):
    def render(self, value):
        if value:
            return shares(value)
        else:
            return '-'


class CurrencyColumn(tables.Column):
    def render(self, value):
        if value:
            return currency(value)
        else:
            return '-'


class PriceColumn(tables.Column):
    def render(self, value):
        if value:
            return price(value)
        else:
            return '-'

class ShareholderTable(tables.Table):
    name = tables.LinkColumn('shareholder_detail', args=[A('slug')])

    class Meta:
        model = Shareholder
        exclude = ('id', 'slug',)
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class SecurityTable(tables.Table):
    name = tables.LinkColumn('security_detail', args=[A('slug')])

    class Meta:
        model = Security
        exclude = ('id', 'slug',)
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class CertificateTable(tables.Table):
    name = tables.LinkColumn('certificate_detail', args=[A('slug')])

    class Meta:
        model = Certificate
        exclude = ('id', 'slug',)
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class InvestorTable(tables.Table):
    name = tables.LinkColumn('investor_detail', args=[A('slug')])

    class Meta:
        model = Investor
        exclude = ('id', 'slug',)
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
