import django_tables2 as tables
from django_tables2.utils import A

# from templatetags.captabletags import percentage, shares, currency, price

from apps.entries.models import (
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


class LiquidationTable(tables.Table):
    name = tables.LinkColumn('investor', args=[A('investor_slug')])
    liquidated = SharesColumn()
    proceeds = CurrencyColumn()
    proceeds_rata = RataColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class FinancingTable(tables.Table):
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

