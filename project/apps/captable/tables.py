import django_tables2 as tables
from django_tables2.utils import A

from templatetags.captabletags import (
    percentage,
    shares,
    currency,
    price,
)

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


class LiquidationTable(tables.Table):
    investor = tables.LinkColumn('investor_detail', args=[A('investor_slug')])
    shareholder = tables.LinkColumn('shareholder_detail', args=[A('shareholder_slug')])
    certificate = tables.LinkColumn('certificate_detail', args=[A('certificate_slug')])
    vested = SharesColumn()
    liquidated = SharesColumn()
    proceeds = CurrencyColumn()
    proceeds_rata = RataColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class FinancingTable(tables.Table):
    security = tables.Column()
    name = tables.Column()
    #pre
    pre_shares = SharesColumn()
    pre_cash = CurrencyColumn()
    pre_price = PriceColumn()
    pre_rata = RataColumn()

    #new cash
    prorata_shares = SharesColumn()
    prorata_cash = CurrencyColumn()

    # converted cash
    converted_shares = SharesColumn()
    converted_cash = CurrencyColumn()
    converted_price = PriceColumn()
    # discounted_cash = CurrencyColumn()

    #post
    post_shares = SharesColumn()
    post_cash = CurrencyColumn()
    post_price = PriceColumn()
    post_rata = RataColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}

