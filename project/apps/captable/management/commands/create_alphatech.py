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
# Securities and Additions
        self.common = CommonSecurity(
            name="Common Stock",
            pre=7000,
            price_per_share=.001,
            date=five_years_ago,
        )

        self.common_addition = AdditionFactory(
            authorized=10000000,
            security=self.common,
            date=five_years_ago,
        )

        self.series_a = PreferredSecurity(
            name="Series A",
            price_per_share=.625,
            seniority=2,
            pre=5000000,
            date=two_years_ago,
        )

        self.series_a_addition = AdditionFactory(
            authorized=10000000,
            security=self.series_a,
            date=two_years_ago,
        )

        self.series_b = PreferredSecurity(
            name="Series B",
            price_per_share=1.72414,
            seniority=3,
            pre=20000000,
            date=one_year_ago,
        )

        self.series_b_addition = AdditionFactory(
            authorized=10000000,
            security=self.series_b,
            date=one_year_ago,
        )

        self.option_plan = OptionSecurity(
            name="Option Plan",
            price_per_share=.10,
            date=five_years_ago,
        )

        self.option_addition1 = AdditionFactory(
            authorized=1000000,
            security=self.option_plan,
            date=five_years_ago,
        )

        self.option_addition2 = AdditionFactory(
            authorized=1900000,
            security=self.option_plan,
            date=one_year_ago,
        )

        self.convertible = ConvertibleSecurity(
            name="Convertible A",
            date=one_year_ago,
            liquidation_preference=1.0,
            price_per_share=1.72414,
            price_cap=20000000,
            discount_rate=.2,
            interest_rate=.1,
            seniority=3,
            pre=20000000,
        )

        self.warrant = WarrantSecurity(
            name="Series A Warrant",
            date=two_years_ago,
            price_per_share=.1,
            seniority=2,
            pre=5000000,
            liquidation_preference=1.0,
            conversion_ratio=1.0,
        )

# Investors
        self.investor1 = InvestorFactory(
            name="Joe Founder",
        )

        self.investor2 = InvestorFactory(
            name="Jane Founder",
        )

        self.investor3 = InvestorFactory(
            name="Venture Partners",
        )

        self.investor4 = InvestorFactory(
            name="Second Round Partners",
        )

        self.investor5 = InvestorFactory(
            name="Bill Furst",
        )

        self.investor6 = InvestorFactory(
            name="Odin Capital",
        )

        self.investor7 = InvestorFactory(
            name="Eric Baker",
        )

# Shareholders
        self.shareholder1 = ShareholderFactory(
            name="Joe Founder",
            investor=self.investor1,
        )

        self.shareholder2 = ShareholderFactory(
            name="Jane Founder",
            investor=self.investor2,
        )

        self.shareholder3 = ShareholderFactory(
            name="VP Fund III",
            investor=self.investor3,
        )

        self.shareholder4 = ShareholderFactory(
            name="SR Fund IV",
            investor=self.investor4,
        )

        self.shareholder5 = ShareholderFactory(
            name="Bill Furst Family Trust",
            investor=self.investor5,
        )

        self.shareholder6 = ShareholderFactory(
            name="Odin Fund 2013",
            investor=self.investor6,
        )

        self.shareholder7 = ShareholderFactory(
            name="Eric Baker",
            investor=self.investor7,
        )


# # Certificates
        self.certificate1 = CertificateFactory(
            security=self.common,
            shareholder=self.shareholder1,
            name='certificate1',
            shares=3500000,
            cash=3500,
            date=five_years_ago,
            vesting_start=five_years_ago,
            vesting_term=48,
            vesting_cliff=12,
        )

        self.certificate2 = CertificateFactory(
            security=self.common,
            shareholder=self.shareholder2,
            name='certificate2',
            shares=3500000,
            cash=3500,
            date=five_years_ago,
            vesting_start=five_years_ago,
            vesting_term=48,
            vesting_cliff=12,
        )

        self.certificate3 = CertificateFactory(
            security=self.series_a,
            shareholder=self.shareholder3,
            name='certificate3',
            shares=1600000,
            cash=1000000,
            is_prorata=True,
            date=two_years_ago,
        )

        self.certificate4 = CertificateFactory(
            security=self.series_b,
            shareholder=self.shareholder4,
            name='certificate4',
            shares=2900000,
            cash=5000000,
            date=one_year_ago,
        )

        self.certificate5 = CertificateFactory(
            security=self.option_plan,
            shareholder=self.shareholder5,
            name='certificate5',
            granted=100000,
            date=two_years_ago,
            vesting_start=two_years_ago,
            vesting_term=48,
            vesting_cliff=12,
        )

        self.certificate6 = CertificateFactory(
            security=self.convertible,
            shareholder=self.shareholder6,
            name='certificate6',
            principal=1000000,
            date=one_year_ago,
            )

        self.certificate7 = CertificateFactory(
            security=self.warrant,
            shareholder=self.shareholder7,
            name='certificate7',
            granted=10000,
            date=two_years_ago,
            vesting_immediate=1,
        )


        self.stdout.write("Successfully created Alpha Tech")
