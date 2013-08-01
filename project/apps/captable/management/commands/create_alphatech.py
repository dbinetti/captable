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

        self.preferred = PreferredSecurity(
            addition__authorized=5000000,
            name="Preferred Stock",
            price_per_share=.5
        )

        self.options = OptionSecurity(
            addition__authorized=1000000,
            name="Option Plan"
        )

        self.investorA = InvestorFactory(
            name="Joe Founder"
        )

        self.investorB = InvestorFactory(
            name="Jane Founder"
        )

        self.investorC = InvestorFactory(
            name="Venture Partners"
        )

        self.shareholderA = ShareholderFactory(
            name="Joe Founder",
            investor=self.investorA
        )

        self.shareholderB = ShareholderFactory(
            name="Jane Founder",
            investor=self.investorB
        )

        self.shareholderC = ShareholderFactory(
            name="VP Fund III",
            investor=self.investorC
        )

        self.certificateA = CertificateFactory(
            security=self.common,
            shareholder=self.shareholderA,
            shares=3500000,
            cash=3500,
            date=one_year_ago,
            vesting_start=one_year_ago
        )

        self.certificateB = CertificateFactory(
            security=self.common,
            shareholder=self.shareholderB,
            shares=3500000,
            cash=3500,
            date=one_year_ago,
            vesting_start=one_year_ago
        )

        self.certificateC = CertificateFactory(
            security=self.preferred,
            shareholder=self.shareholderC,
            shares=2000000,
            cash=1000000,
            date=one_year_ago,
            vesting_start=one_year_ago
        )

        self.stdout.write("Successfully created Alpha Tech")
