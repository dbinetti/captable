from django.core.management.base import BaseCommand

from apps.captable.factories import *

import datetime
from dateutil.relativedelta import relativedelta


# Time-based globals
today = datetime.date.today()
six_months_ago = today - relativedelta(months=6)
one_year_ago = today - relativedelta(years=1)
two_years_ago = today - relativedelta(years=2)
five_years_ago = today - relativedelta(years=5)


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.common = CommonSecurity(
            addition__authorized=100000000,
            name="Common Stock"
        )

        self.seriesA = PreferredSecurity(
            addition__authorized=5000000,
            name="Series A",
            price_per_share=.5
        )

        self.seriesB = PreferredSecurity(
            addition__authorized=5000000,
            name="Series B",
            price_per_share=1
        )

        self.options = OptionSecurity(
            addition__authorized=1000000,
            name="Option Plan"
        )

        self.investor_common1 = InvestorFactory(
            name="Joe Founder"
        )

        self.investor_common2 = InvestorFactory(
            name="Jane Founder"
        )

        self.investor_seriesA1 = InvestorFactory(
            name="Venture Partners"
        )

        self.investor_seriesB1 = InvestorFactory(
            name="Second Round Partners"
        )

        self.investor_option1 = InvestorFactory(
            name="Bill Furst"
        )

        self.shareholder_common1 = ShareholderFactory(
            name="Joe Founder",
            investor=self.investor_common1
        )

        self.shareholder_common2 = ShareholderFactory(
            name="Jane Founder",
            investor=self.investor_common2
        )

        self.shareholder_seriesA1 = ShareholderFactory(
            name="VP Fund III",
            investor=self.investor_seriesA1
        )

        self.shareholder_seriesB1 = ShareholderFactory(
            name="SR Fund IV",
            investor=self.investor_seriesB1
        )

        self.shareholder_option1 = ShareholderFactory(
            name="Bill Furst Family Trust",
            investor=self.investor_option1,
        )

        self.certificateCS01 = CertificateFactory(
            security=self.common,
            shareholder=self.shareholder_common1,
            shares=3500000,
            cash=3500,
            date=five_years_ago,
            vesting_start=five_years_ago
        )

        self.certificateCS02 = CertificateFactory(
            security=self.common,
            shareholder=self.shareholder_common2,
            shares=3500000,
            cash=3500,
            date=five_years_ago,
            vesting_start=five_years_ago
        )

        self.certificatePA01 = CertificateFactory(
            security=self.seriesA,
            shareholder=self.shareholder_seriesA1,
            shares=2000000,
            cash=1000000,
            is_prorata=True,
            date=two_years_ago,
            vesting_start=two_years_ago
        )

        self.certificatePB01 = CertificateFactory(
            security=self.seriesB,
            shareholder=self.shareholder_seriesB1,
            shares=10000000,
            cash=10000000,
            date=one_year_ago,
            vesting_start=one_year_ago
        )

        self.certificateOP01 = CertificateFactory(
            security=self.options,
            shareholder=self.shareholder_option1,
            granted=100000,
            date=two_years_ago,
            vesting_start=two_years_ago
        )

        self.stdout.write("Successfully created Alpha Tech")
