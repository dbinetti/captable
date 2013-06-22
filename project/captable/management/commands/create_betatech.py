from django.core.management.base import BaseCommand

from captable.factories import *

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

        self.company = CompanyFactory(
            name="Beta Tech",
            slug="beta-tech")

        self.common = CommonSecurity(
            addition__authorized=100000000,
            name="Common Stock",
            company=self.company)

        self.convertible = ConvertibleSecurity(
            name="Convertible Debt",
            company=self.company,
            default_conversion_price=.5,
            price_cap=5000000)

        self.options = OptionSecurity(
            addition__authorized=1000000,
            name="Option Plan",
            company=self.company)

        self.investorA = InvestorFactory(
            name="Sam Founder")

        self.investorB = InvestorFactory(
            name="Sarah Founder")

        self.investorC = InvestorFactory(
            name="Peter Angel")

        self.shareholderA = ShareholderFactory(
            name="Sam Founder",
            investor=self.investorA)

        self.shareholderB = ShareholderFactory(
            name="Sarah Founder",
            investor=self.investorB)

        self.shareholderC = ShareholderFactory(
            name="Peter Angel",
            investor=self.investorC)

        self.transactionA = TransactionFactory(
            security=self.common,
            shareholder=self.shareholderA,
            shares=3500000,
            cash=3500,
            date=one_year_ago,
            vesting_start=one_year_ago)

        self.transactionB = TransactionFactory(
            security=self.common,
            shareholder=self.shareholderB,
            shares=3500000,
            cash=3500,
            date=one_year_ago,
            vesting_start=one_year_ago)

        self.transactionC = TransactionFactory(
            security=self.convertible,
            shareholder=self.shareholderC,
            debt=1000000,
            date=one_year_ago,
            vesting_start=one_year_ago)

        self.stdout.write("Successfully created Beta Tech")
