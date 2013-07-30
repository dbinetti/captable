import django_tables2 as tables
from django_tables2.utils import A


from templatetags.captabletags import percentage, shares, currency, price


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

# class InvestorsTable(tables.Table):
#     # name = tables.LinkColumn('investor', args=[A('investor.shareholder.certificate.security.company.slug'), A('id')])
#     name = tables.Column()
#     class Meta:
#         attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ShareholdersTable(tables.Table):
    name = tables.LinkColumn('shareholder', args=[A('slug')])
    investor = tables.LinkColumn('investor', args=[A('investor.slug')])

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


# class SecuritiesTable(tables.Table):
#     name = tables.LinkColumn('security', args=[A('company.slug'), A('slug')])

#     class Meta:
#         attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


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


class CertificateTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    current = SharesColumn()
    purchase = CurrencyColumn()
    date = tables.DateColumn()
    status = tables.Column()
    is_transferred = tables.BooleanColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class CommonTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    date = tables.DateColumn()
    shareholder = tables.LinkColumn('shareholder', args=[A('shareholder.slug')])
    shares = SharesColumn()
    returned = SharesColumn()
    outstanding_shares = SharesColumn()
    vested = SharesColumn()
    cash = CurrencyColumn()
    refunded = CurrencyColumn()
    status = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class PreferredTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    date = tables.DateColumn()
    shareholder = tables.LinkColumn('shareholder', args=[A('shareholder.slug')])
    shares = SharesColumn()
    returned = SharesColumn()
    outstanding_shares = SharesColumn()
    cash = CurrencyColumn()
    refunded = CurrencyColumn()
    # discounted_price = PriceColumn()
    preference = CurrencyColumn()
    status = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ConvertibleTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    date = tables.DateColumn()
    shareholder = tables.LinkColumn('shareholder', args=[A('shareholder.slug')])
    debt = CurrencyColumn()
    accrued = CurrencyColumn()
    forgiven = CurrencyColumn()
    converted_date = tables.DateColumn()
    discounted = CurrencyColumn()
    liquidated = SharesColumn()
    status = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class WarrantTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    date = tables.DateColumn()
    shareholder = tables.LinkColumn('shareholder', args=[A('shareholder.slug')])
    granted = SharesColumn()
    exercised = SharesColumn()
    cancelled = SharesColumn()
    outstanding_warrants = SharesColumn()
    # purchase = CurrencyColumn()
    status = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class OptionTable(tables.Table):
    name = tables.LinkColumn('certificate', args=[A('name')])
    date = tables.DateColumn()
    shareholder = tables.LinkColumn('shareholder', args=[A('shareholder.slug')])
    granted = SharesColumn()
    exercised = SharesColumn()
    cancelled = SharesColumn()
    outstanding_options = SharesColumn()
    vested = SharesColumn()
    status = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
