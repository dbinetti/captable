from __future__ import division

from django.test import TestCase

from apps.captable.factories import *

import datetime
from dateutil.relativedelta import relativedelta


# Time-based globals
today = datetime.date.today()
six_months_ago = today - relativedelta(months=6)
one_year_ago = today - relativedelta(years=1)
two_years_ago = today - relativedelta(years=2)
five_years_ago = today - relativedelta(years=5)



class MainTests(TestCase):
    def setUp(self):
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


# Certificates
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


# Investor Class
    def test_investor_get_absolute_url(self):
        self.assertEqual(self.investor1.get_absolute_url(), '/investor/joe-founder/')


    def test_investor_proceeds(self):
        self.assertEqual(round(self.investor1.proceeds(10000000),2), 1439713.33)
        self.assertEqual(round(self.investor2.proceeds(10000000),2), 1439713.33)
        self.assertEqual(round(self.investor3.proceeds(10000000),2), 993788.82)
        self.assertEqual(round(self.investor4.proceeds(10000000),2), 5000006)
        self.assertEqual(round(self.investor5.proceeds(10000000),2), 20567.33)
        self.assertEqual(round(self.investor6.proceeds(10000000),2), 1100000)
        self.assertEqual(round(self.investor7.proceeds(10000000),2), 6211.18)

    def test_investor_liquidated(self):
        self.assertEqual(self.investor1.liquidated, 3500000)
        self.assertEqual(self.investor2.liquidated, 3500000)
        self.assertEqual(self.investor3.liquidated, 1600000)
        self.assertEqual(self.investor4.liquidated, 2900000)
        self.assertEqual(self.investor5.liquidated, 50000)
        self.assertEqual(round(self.investor6.liquidated), 637999)
        self.assertEqual(self.investor7.liquidated, 10000)

    def test_investor_outstanding(self):
        self.assertEqual(self.investor1.outstanding, 3500000)
        self.assertEqual(self.investor2.outstanding, 3500000)
        self.assertEqual(self.investor3.outstanding, 1600000)
        self.assertEqual(self.investor4.outstanding, 2900000)
        self.assertEqual(self.investor5.outstanding, 100000)
        self.assertEqual(self.investor6.outstanding, 0)
        self.assertEqual(self.investor7.outstanding, 10000)

    def test_investor_paid(self):
        self.assertEqual(self.investor1.paid, 3500)
        self.assertEqual(self.investor2.paid, 3500)
        self.assertEqual(self.investor3.paid, 1000000)
        self.assertEqual(self.investor4.paid, 5000000)
        self.assertEqual(self.investor5.paid, 0)
        self.assertEqual(self.investor6.paid, 1000000)
        self.assertEqual(self.investor7.paid, 0)

    def test_investor_preference(self):
        self.assertEqual(self.investor1.preference, 0)
        self.assertEqual(self.investor2.preference, 0)
        self.assertEqual(self.investor3.preference, 1000000)
        self.assertEqual(self.investor4.preference, 5000006)
        self.assertEqual(self.investor5.preference, 0)
        self.assertEqual(self.investor6.preference, 1100000)
        self.assertEqual(self.investor7.preference, 0)

    def test_investor_proceeds_rata(self):
        self.assertEqual(round(self.investor1.proceeds_rata(10000000),2), .1400)
        self.assertEqual(round(self.investor2.proceeds_rata(10000000),2), .1400)
        self.assertEqual(round(self.investor3.proceeds_rata(10000000),2), .1000)
        self.assertEqual(round(self.investor4.proceeds_rata(10000000),2), .5000)
        self.assertEqual(round(self.investor5.proceeds_rata(10000000),2), .0000)
        self.assertEqual(round(self.investor6.proceeds_rata(10000000),2), .1100)
        self.assertEqual(round(self.investor7.proceeds_rata(10000000),2), .0000)

    def test_investor_prorata(self):
        self.assertEqual(round(self.investor1.prorata(1000000)), 0)
        self.assertEqual(round(self.investor2.prorata(1000000)), 0)
        self.assertEqual(round(self.investor3.prorata(1000000)), 106326)
        self.assertEqual(round(self.investor4.prorata(1000000)), 0)
        self.assertEqual(round(self.investor5.prorata(1000000)), 0)
        self.assertEqual(round(self.investor6.prorata(1000000)), 0)
        self.assertEqual(round(self.investor7.prorata(1000000)), 0)

    def test_investor_exchanged(self):
        self.assertEqual(round(self.investor1.exchanged()), 0)
        self.assertEqual(round(self.investor2.exchanged()), 0)
        self.assertEqual(round(self.investor3.exchanged()), 0)
        self.assertEqual(round(self.investor4.exchanged()), 0)
        self.assertEqual(round(self.investor5.exchanged()), 0)
        self.assertEqual(round(self.investor6.exchanged()), 637999)
        self.assertEqual(round(self.investor7.exchanged()), 0)



# Security Class
    def test_security_get_absolute_url(self):
        self.assertEqual(self.common.get_absolute_url(), '/security/common-stock/')

    def test_security_security_class(self):
        self.assertEqual(self.common.security_class, 'Equity')
        self.assertEqual(self.option_plan.security_class, 'Rights')
        self.assertEqual(self.series_a.security_class, 'Equity')
        self.assertEqual(self.series_b.security_class, 'Equity')
        self.assertEqual(self.warrant.security_class, 'Rights')
        self.assertEqual(self.convertible.security_class, 'Debt')

    def test_security_authorized(self):
        self.assertEqual(self.common.authorized, 10000000)
        self.assertEqual(self.option_plan.authorized, 2900000)
        self.assertEqual(self.series_a.authorized, 10000000)
        self.assertEqual(self.series_b.authorized, 10000000)
        self.assertEqual(self.convertible.authorized, None)
        self.assertEqual(self.warrant.authorized, None)

    def test_security_available(self):
        self.assertEqual(self.option_plan.available, 2800000)

    def test_security_outstanding(self):
        self.assertEqual(self.common.outstanding, 7000000)
        self.assertEqual(self.option_plan.outstanding, 100000)
        self.assertEqual(self.series_a.outstanding, 1600000)
        self.assertEqual(self.series_b.outstanding, 2900000)
        self.assertEqual(self.convertible.outstanding, 0)
        self.assertEqual(self.warrant.outstanding, 10000)

    def test_security_outstanding_rata(self):
        self.assertEqual(round(self.common.outstanding_rata, 4), .6029)
        self.assertEqual(round(self.option_plan.outstanding_rata, 4), .0086)
        self.assertEqual(round(self.series_a.outstanding_rata, 4), .1378)
        self.assertEqual(round(self.series_b.outstanding_rata, 4), .2498)
        self.assertEqual(round(self.convertible.outstanding_rata, 4), 0)
        self.assertEqual(round(self.warrant.outstanding_rata, 4), .0009)

    def test_security_converted(self):
        self.assertEqual(self.common.converted, 7000000)
        self.assertEqual(self.option_plan.converted, 0)
        self.assertEqual(self.series_a.converted, 1600000)
        self.assertEqual(self.series_b.converted, 2900000)
        self.assertEqual(round(self.convertible.converted), 637999)
        self.assertEqual(self.warrant.converted, 0)

    def test_security_converted_rata(self):
        self.assertEqual(round(self.common.converted_rata, 4), .5767)
        self.assertEqual(round(self.option_plan.converted_rata, 4), .0)
        self.assertEqual(round(self.series_a.converted_rata, 4), .1318)
        self.assertEqual(round(self.series_b.converted_rata, 4), .2389)
        self.assertEqual(round(self.convertible.converted_rata, 4), .0526)
        self.assertEqual(round(self.warrant.converted_rata, 4), .0000)

    def test_security_diluted(self):
        self.assertEqual(self.common.diluted, 7000000)
        self.assertEqual(self.option_plan.diluted, 2900000)
        self.assertEqual(self.series_a.diluted, 1600000)
        self.assertEqual(self.series_b.diluted, 2900000)
        self.assertEqual(round(self.convertible.diluted), 637999)
        self.assertEqual(self.warrant.diluted, 10000)

    def test_security_diluted_rata(self):
        self.assertEqual(round(self.common.diluted_rata, 4), .4621)
        self.assertEqual(round(self.option_plan.diluted_rata, 4), .1914)
        self.assertEqual(round(self.series_a.diluted_rata, 4), .1056)
        self.assertEqual(round(self.series_b.diluted_rata, 4), .1914)
        self.assertEqual(round(self.convertible.diluted_rata, 4), .0421)
        self.assertEqual(round(self.warrant.diluted_rata, 4), .0007)


# Addition Class
    def test_addition_unicode(self):
        self.assertEqual(self.common_addition.__unicode__(), '10,000,000 of Common Stock on {0}'.format(five_years_ago))

# Certificate Class
    def test_certificate_unicode(self):
        self.assertEqual(self.certificate1.__unicode__(), 'certificate1 - Joe Founder')

    def test_certificate_get_absolute_url(self):
        self.assertEqual(self.certificate1.get_absolute_url(), '/certificate/certificate1/')

    def test_certificate_vested(self):
        self.assertEqual(self.certificate3.vested, 1600000)
        self.assertEqual(round(self.certificate6.vested), 637999)

    def test_certificate_outstanding(self):
        self.assertEqual(self.certificate1.outstanding, 3500000)
        self.assertEqual(self.certificate2.outstanding, 3500000)
        self.assertEqual(self.certificate3.outstanding, 1600000)
        self.assertEqual(self.certificate4.outstanding, 2900000)
        self.assertEqual(self.certificate5.outstanding, 100000)
        self.assertEqual(self.certificate6.outstanding, 0)
        self.assertEqual(self.certificate7.outstanding, 10000)

    def test_certificate_paid(self):
        self.assertEqual(self.certificate1.paid, 3500)
        self.assertEqual(self.certificate2.paid, 3500)
        self.assertEqual(self.certificate3.paid, 1000000)
        self.assertEqual(self.certificate4.paid, 5000000)
        self.assertEqual(self.certificate5.paid, 0)
        self.assertEqual(self.certificate6.paid, 1000000)
        self.assertEqual(self.certificate7.paid, 0)

    def test_certificate_converted(self):
        self.assertEqual(self.certificate1.converted, 3500000)
        self.assertEqual(self.certificate2.converted, 3500000)
        self.assertEqual(self.certificate3.converted, 1600000)
        self.assertEqual(self.certificate4.converted, 2900000)
        self.assertEqual(self.certificate5.converted, 0)
        self.assertEqual(round(self.certificate6.converted), 637999)
        self.assertEqual(self.certificate7.converted, 0)

    def test_certificate_diluted(self):
        self.assertEqual(self.certificate1.diluted, 3500000)
        self.assertEqual(self.certificate2.diluted, 3500000)
        self.assertEqual(self.certificate3.diluted, 1600000)
        self.assertEqual(self.certificate4.diluted, 2900000)
        self.assertEqual(self.certificate5.diluted, 100000)
        self.assertEqual(round(self.certificate6.diluted), 637999)
        self.assertEqual(self.certificate7.diluted, 10000)

    def test_certificate_liquidated(self):
        self.assertEqual(self.certificate1.liquidated, 3500000)
        self.assertEqual(self.certificate2.liquidated, 3500000)
        self.assertEqual(self.certificate3.liquidated, 1600000)
        self.assertEqual(self.certificate4.liquidated, 2900000)
        self.assertEqual(self.certificate5.liquidated, 50000)
        self.assertEqual(round(self.certificate6.liquidated), 637999)
        self.assertEqual(self.certificate7.liquidated, 10000)

    def test_certificate_preference(self):
        self.assertEqual(self.certificate1.preference, 0)
        self.assertEqual(self.certificate2.preference, 0)
        self.assertEqual(self.certificate3.preference, 1000000)
        self.assertEqual(self.certificate4.preference, 5000006)
        self.assertEqual(self.certificate5.preference, 0)
        self.assertEqual(self.certificate6.preference, 1100000)
        self.assertEqual(self.certificate7.preference, 0)

    def test_certificate_accrued(self):
        self.assertEqual(self.certificate1.accrued, None)
        self.assertEqual(self.certificate2.accrued, None)
        self.assertEqual(self.certificate3.accrued, None)
        self.assertEqual(self.certificate4.accrued, None)
        self.assertEqual(self.certificate5.accrued, None)
        self.assertEqual(self.certificate6.accrued, 1100000)
        self.assertEqual(self.certificate7.accrued, None)

    def test_certificate_discounted(self):
        self.assertEqual(self.certificate1.discounted(), 0)
        self.assertEqual(self.certificate2.discounted(), 0)
        self.assertEqual(self.certificate3.discounted(), 0)
        self.assertEqual(self.certificate4.discounted(), 0)
        self.assertEqual(self.certificate5.discounted(), 0)
        self.assertEqual(self.certificate6.discounted(), 1375000.0)
        # TODO double-cbeck this and look at all permutations.
        self.assertEqual(self.certificate7.discounted(), 0)

    def test_certificate_exchanged(self):
        self.assertEqual(self.certificate1.exchanged(),0)
        self.assertEqual(self.certificate2.exchanged(),0)
        self.assertEqual(self.certificate3.exchanged(),0)
        self.assertEqual(self.certificate4.exchanged(),0)
        self.assertEqual(self.certificate5.exchanged(),0)
        self.assertEqual(round(self.certificate6.exchanged()),637999)
        self.assertEqual(self.certificate7.exchanged(),0)

        # test price cap
        self.assertEqual(round(self.certificate6.exchanged(40000000,2.62314)),838690)

    def test_certificate_prorata(self):
        self.assertEqual(self.certificate1.prorata(1000000),0)
        self.assertEqual(self.certificate2.prorata(1000000),0)
        self.assertEqual(round(self.certificate3.prorata(1000000)),106326)
        self.assertEqual(self.certificate4.prorata(1000000),0)
        self.assertEqual(self.certificate5.prorata(1000000),0)
        self.assertEqual(self.certificate6.prorata(1000000),0)
        self.assertEqual(self.certificate7.prorata(1000000),0)

    def test_certificate_proceeds(self):
        self.assertEqual(round(self.certificate1.proceeds(25000000),2),7173307.55)
        self.assertEqual(round(self.certificate2.proceeds(25000000),2),7173307.55)
        self.assertEqual(round(self.certificate3.proceeds(25000000),2),3279226.31)
        self.assertEqual(round(self.certificate4.proceeds(25000000),2),5943597.68)
        self.assertEqual(round(self.certificate5.proceeds(25000000),2),102475.82)
        self.assertEqual(round(self.certificate6.proceeds(25000000),2),1307589.92)
        self.assertEqual(round(self.certificate7.proceeds(25000000),2),20495.16)

