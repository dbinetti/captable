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
        self.common = CommonSecurity(
            name="Common Stock",
            pre=7000,
            price_per_share=.001,
            date=five_years_ago
        )

        self.expansion_common = AdditionFactory(
            authorized=10000000,
            security=self.common,
            date=five_years_ago,
        )

        self.seriesA = PreferredSecurity(
            name="Series A",
            price_per_share=.625,
            seniority=2,
            pre=5000000,
            date=two_years_ago
        )

        self.expansion_seriesA = AdditionFactory(
            authorized=10000000,
            security=self.seriesA,
            date=two_years_ago,
        )

        self.seriesB = PreferredSecurity(
            name="Series B",
            price_per_share=1.72414,
            seniority=3,
            pre=20000000,
            date=one_year_ago
        )

        self.expansion_seriesB = AdditionFactory(
            authorized=10000000,
            security=self.seriesB,
            date=one_year_ago,
        )

        self.options = OptionSecurity(
            name="Option Plan",
            price_per_share=.10,
            date=five_years_ago,
        )

        self.expansion1 = AdditionFactory(
            authorized=1000000,
            security=self.options,
            date=five_years_ago,
        )

        self.expansion2 = AdditionFactory(
            authorized=1900000,
            security=self.options,
            date=one_year_ago
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
            shares=1600000,
            cash=1000000,
            is_prorata=True,
            date=two_years_ago,
        )

        self.certificatePB01 = CertificateFactory(
            security=self.seriesB,
            shareholder=self.shareholder_seriesB1,
            shares=2900000,
            cash=5000000,
            date=one_year_ago,
        )

        self.certificateOP01 = CertificateFactory(
            security=self.options,
            shareholder=self.shareholder_option1,
            granted=100000,
            date=two_years_ago,
            vesting_start=two_years_ago
        )


    def test_preference(self):
        self.assertEqual(self.common.pre, 7000)



























# from __future__ import division

# import datetime
# from dateutil.relativedelta import relativedelta

# from django.test import TestCase

# from apps.captable.models import *
# from apps.captable.constants import *
# from apps.captable.factories import *

# # Time-based globals
# today = datetime.date.today()
# six_months_ago = today - relativedelta(months=6)
# one_year_ago = today - relativedelta(years=1)
# two_years_ago = today - relativedelta(years=2)
# five_years_ago = today - relativedelta(years=5)


# class ModelTests(TestCase):

#     def setUp(self):

#         self.common = TransactionFactory(
#             security__name="Common Security",
#             shares=100)

#         self.preferred = TransactionFactory(
#             security__name="Test Preferred",
#             security__security_type=SECURITY_TYPE_PREFERRED,
#             cash=100,
#             shares=100,
#             security__price_per_share=1,
#             security__liquidation_preference=1.0,
#             shareholder__investor__is_prorata=True,
#             security__conversion_ratio=1.0)

#         self.convertible = TransactionFactory(
#             security__name="Test Convertible",
#             security__security_type=SECURITY_TYPE_CONVERTIBLE,
#             security__interest_rate=.1,
#             security__default_conversion_price=1,
#             date=one_year_ago,
#             security__price_cap=1000,
#             security__discount_rate=.2,
#             debt=100)

#         self.option = TransactionFactory(
#             security__name="Test Option",
#             security__security_type=SECURITY_TYPE_OPTION,
#             rights=100)

#         self.warrant = TransactionFactory(
#             security__name="Test Warrant",
#             security__security_type=SECURITY_TYPE_WARRANT,
#             rights=100)

#         self.converted = TransactionFactory(
#             security__name="Test Converted",
#             security__security_type=SECURITY_TYPE_CONVERTIBLE,
#             security__interest_rate=.1,
#             security__is_converted=True,
#             date=one_year_ago,
#             debt=100)

#         self.common_no_cliff = TransactionFactory(
#             security__name="Test Common",
#             shares=100,
#             date=six_months_ago,
#             vesting_start=six_months_ago,
#             vesting_term=4.0,
#             vesting_cliff=1.0,
#             vesting_immediate=0.0)

#         self.common_half_vested = TransactionFactory(
#             security__name="Test Common",
#             shares=100,
#             date=two_years_ago,
#             vesting_start=two_years_ago,
#             vesting_term=4.0,
#             vesting_cliff=1.0,
#             vesting_immediate=0.0)

#         self.common_fully_vested = TransactionFactory(
#             security__name="Test Common",
#             shares=100,
#             date=five_years_ago,
#             vesting_start=five_years_ago,
#             vesting_term=4.0,
#             vesting_cliff=1.0,
#             vesting_immediate=0.0)

#         self.option_fully_vested = TransactionFactory(
#             security__name="Test Option",
#             rights=100,
#             date=five_years_ago,
#             vesting_start=five_years_ago,
#             vesting_term=4.0,
#             vesting_cliff=1.0,
#             vesting_immediate=0.0)

#         self.common_single_trigger = TransactionFactory(
#             security__name="Test Common",
#             shares=100,
#             date=six_months_ago,
#             vesting_start=six_months_ago,
#             vesting_term=4.0,
#             vesting_cliff=1.0,
#             vesting_immediate=0.0,
#             vesting_trigger=TRIGGER_SINGLE)

#         self.founder_vesting = TransactionFactory(
#             security__name="Test Common",
#             shares=100,
#             date=one_year_ago,
#             vesting_start=one_year_ago,
#             vesting_term=3.0,
#             vesting_cliff=0.0,
#             vesting_immediate=.25)

#         self.proforma = TransactionFactory(
#             security__name="Proforma",
#             shares=100,
#             security__security_type=SECURITY_TYPE_PREFERRED,
#             security__is_proforma=True)

# # Transaction Model Tests
# # -----------------------

#     def test_vested(self):
#         """Tests the vested portion of investor holdings"""
#         self.assertEqual(self.common_no_cliff.vested, 0)
#         self.assertEqual(self.common_half_vested.vested, 50)
#         self.assertEqual(self.common_fully_vested.vested, 100)
#         self.assertEqual(self.preferred.vested, 100)
#         self.assertEqual(self.convertible.vested, 110)
#         self.assertEqual(self.option_fully_vested.vested, 100)
#         self.assertEqual(self.common_single_trigger.vested, 100)
#         self.assertEqual(self.founder_vesting.vested, 50)
#         self.assertEqual(self.converted.vested, None)
#         self.assertEqual(self.proforma.vested, None)

#     def test_converted(self):
#         """Tests the converted portion of a transaction"""
#         self.assertEqual(self.proforma.converted, None)
#         self.assertEqual(self.converted.converted, None)
#         self.assertEqual(self.preferred.converted, 100)
#         self.assertEqual(self.convertible.converted, 110)
#         self.assertEqual(self.option.converted, 100)
#         self.assertEqual(self.warrant.converted, 100)
#         self.assertEqual(self.common.converted, 100)

#     def test_preference(self):
#         """Tests the amount of investor preference"""
#         self.assertEqual(self.preferred.preference, 100)
#         self.assertEqual(self.common.preference, None)
#         self.assertEqual(self.convertible.preference, 110)

#     def test_accrued(self):
#         """Tests the accrued convertible interest."""
#         self.assertEqual(self.convertible.accrued, 110)
#         self.assertEqual(self.common.accrued, None)
#         self.assertEqual(self.converted.accrued, 110)

#     def test_discounted(self):
#         """Tests the discounted convertible value"""
#         self.assertEqual(self.convertible.discounted(), 110)
#         self.assertEqual(self.proforma.discounted(), None)
#         self.assertEqual(self.converted.discounted(), None)
#         self.assertEqual(self.common.discounted(), None)
#         self.assertEqual(self.convertible.discounted(500), 137.5)
#         self.assertEqual(self.convertible.discounted(2000), 220)

#     def test_exchanged(self):
#         """Tests the number of shares from a converted debt instrument"""
#         self.assertEqual(self.proforma.exchanged, None)
#         self.assertEqual(self.converted.exchanged, None)
#         self.assertEqual(self.common.exchanged, None)
#         self.assertEqual(self.convertible.exchanged, 110)

#     def test_proceeds(self):
#         """Tests the proceeds from a transaction"""
#         self.assertEqual(self.proforma.proceeds(1000), None)

# # Transaction Model Manager Tests
# # -------------------------------

#     def test_manager_outstanding(self):
#         """Tests the manager for outstanding shares"""
#         self.assertEqual(self.common.security.company.outstanding, 800)

#     def test_manager_converted(self):
#         """Tests the manager for converted shares"""
#         self.assertEqual(Transaction.objects.converted, 1110)

#     def test_manager_vested(self):
#         """Tests the manager for vested shares"""
#         self.assertEqual(Transaction.objects.vested, 610)

#     def test_manager_accrued(self):
#         """Tests the manager for accrued debt"""
#         self.assertEqual(Transaction.objects.accrued, 220)

#     def test_manager_granted(self):
#         """Tests the manager for granted shares"""
#         self.assertEqual(self.common.security.company.granted, 200)

#     def test_manager_available(self):
#         """Tests the manager for available shares"""
#         self.assertEqual(self.common.security.company.available, 800)

#     def test_manager_preference(self):
#         """Tests the manager for investor preference"""
#         self.assertEqual(Transaction.objects.preference, 210)

#     def test_manager_diluted(self):
#         """Tests the manager for diluted shares"""
#         self.assertEqual(self.common.security.company.diluted, 2010)

#     def test_manager_discounted(self):
#         """Tests the manager for discounted debt"""
#         self.assertEqual(Transaction.objects.discounted(), 110)

# # Security Model Tests
# # --------------------

#     def test_security_class(self):
#         """Tests the security class property"""
#         self.assertEqual(self.common.security.security_class, "Equity")
#         self.assertEqual(self.preferred.security.security_class, "Equity")
#         self.assertEqual(self.convertible.security.security_class, "Debt")
#         self.assertEqual(self.option.security.security_class, "Rights")
#         self.assertEqual(self.warrant.security.security_class, "Rights")

# # Security Model Manager Tests
# # ----------------------------

#     def test_option_pool(self):
#         """Tests the option pool"""
#         self.assertEqual(self.common.security.company.pool, 1000)

# # Tranch Model Manager Tests
# # --------------------------

#     def test_price(self):
#         # TODO Important test here.  Think this one out clearly.
#         pass

# # Form Tests
# # --------------------------

#     def test_financing_form(self):
#         # Test Stub
#         pass

#     def test_liquidation_form(self):
#         # Test Stub
#         pass

# # View Tests
# # --------------------------

#     def test_summary_login(self):
#         # Test Stub
#         pass


# class ConversionRatio(TestCase):

#     def setUp(self):
#         self.common = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100,
#             vesting_immediate=1)

#         self.preferred = PreferredSecurity(
#             conversion_ratio=2.0)

#         self.preferredTransaction = TransactionFactory(
#             security=self.preferred,
#             shares=100)

#     def test_conversion_ratio_proceeds(self):
#         self.assertEqual(self.preferredTransaction.proceeds(900), 600)


# class FullParticipationTests(TestCase):

#     def setUp(self):

#         self.preferred = PreferredSecurity(
#             is_participating=True,
#             participation_cap=0.0)

#         self.commonTransaction = TransactionFactory(
#             security__security_type=SECURITY_TYPE_COMMON,
#             shares=100,
#             vesting_immediate=1)

#         self.preferredTransaction = TransactionFactory(
#             security=self.preferred,
#             cash=100,
#             shares=100)

#     def test_full_participation_proceeds(self):
#         self.assertEqual(self.preferredTransaction.proceeds(1000), 550)
#         self.assertEqual(self.preferredTransaction.proceeds(100), 100)
#         self.assertEqual(self.commonTransaction.proceeds(1000), 450)
#         self.assertEqual(self.commonTransaction.proceeds(100), 0)
#         self.assertEqual(self.preferredTransaction.proceeds(50), 50)
#         self.assertEqual(self.commonTransaction.proceeds(50), 0)


# class CappedParticipationTests(TestCase):

#     def setUp(self):

#         self.preferred = PreferredSecurity(
#             is_participating=True,
#             participation_cap=3.0)

#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100,
#             vesting_immediate=1)

#         self.preferredTransaction = TransactionFactory(
#             security=self.preferred,
#             cash=100,
#             shares=100)

#     def test_capped_participation_proceeds(self):
#         self.assertEqual(self.preferredTransaction.proceeds(100), 100)
#         self.assertEqual(self.preferredTransaction.proceeds(1000), 500)
#         self.assertEqual(self.preferredTransaction.proceeds(200), 150)
#         self.assertEqual(self.commonTransaction.proceeds(100), 0)
#         self.assertEqual(self.commonTransaction.proceeds(1000), 500)
#         self.assertEqual(self.commonTransaction.proceeds(200), 50)


# class LiquidationPreferenceTests(TestCase):

#     def setUp(self):

#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100,
#             vesting_immediate=1)

#         self.preferred = PreferredSecurity(
#             liquidation_preference=2.0)

#         self.preferredTransaction = TransactionFactory(
#             security=self.preferred,
#             shares=100)

#     def test_liquidation_preference(self):
#         self.assertEqual(self.preferredTransaction.proceeds(1000), 500)
#         self.assertEqual(self.preferredTransaction.proceeds(150), 150)
#         self.assertEqual(self.commonTransaction.proceeds(1000), 500)
#         self.assertEqual(self.commonTransaction.proceeds(150), 0)


# class NoCommonVested(TestCase):

#     def setUp(self):

#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100,
#             vesting_start=today - relativedelta(months=6))

#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=100)

#     def test_no_vesting(self):
#         self.assertEqual(self.preferredTransaction.proceeds(1000), 1000)


# class OptionPool(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)

#         self.optionPool = OptionSecurity()

#         self.optionTransaction = TransactionFactory(
#             security__name="Option Security",
#             rights=100)

#     def test_option_pool(self):
#         self.assertEqual(self.commonTransaction.security.company.pool, 200)
#         self.assertEqual(self.commonTransaction.security.company.granted, 100)
#         self.assertEqual(self.commonTransaction.security.company.available, 100)


# class NoOptionPool(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             vesting_trigger=TRIGGER_SINGLE,
#             shares=100)

#     def test_no_option_pool(self):
#         self.assertEqual(self.commonTransaction.security.company.pool, None)

#     def test_total_proceeds(self):
#         self.assertEqual(Transaction.objects.proceeds(1000), 1000)

#     def test_liquidated(self):
#         self.assertEqual(self.commonTransaction.liquidated, 100)


# class Convertible(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=100)
#         self.convertibleTransaction = TransactionFactory(
#             security=ConvertibleSecurity(),
#             date=one_year_ago,
#             debt=82)
#         self.convertibleTransaction2 = TransactionFactory(
#             security=ConvertibleSecurity(),
#             date=one_year_ago,
#             debt=82)

#     def test_upgraded_convertibles(self):
#         self.assertEqual(int(self.convertibleTransaction.upgraded(1000, 1)), 100)
#         self.assertEqual(int(Transaction.objects.upgraded(1000, 1)), 200)

#     def test_manager_exchanged(self):
#         """Tests the manager for exchanged debt in shares"""
#         self.assertEqual(Transaction.objects.exchanged, 1804)
#         self.assertEqual(self.convertibleTransaction.liquidated, 902)


# class Prorata(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)
#         self.shareholder = ShareholderFactory(
#             name="Prorata Shareholder",
#             investor__name="Prorata Investor",
#             investor__is_prorata=1)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shareholder=self.shareholder,
#             shares=100)

#     def test_prorata(self):
#         """Tests the shares returned from an investor's prorata"""
#         self.assertEqual(self.preferredTransaction.prorata(100), 50)
#         self.assertEqual(Transaction.objects.prorata(100), 50)


# class StoppedVesting(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100,
#             vesting_start=five_years_ago,
#             vesting_stop=two_years_ago)

#     def test_vesting_stop(self):
#         self.assertEqual(self.commonTransaction.vested, 75)


# class ProformaCheck(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)
#         self.proformaTransaction = TransactionFactory(
#             security__is_proforma=True,
#             security__security_type=SECURITY_TYPE_PREFERRED,
#             shares=100,
#             security__price_per_share=1)

#     def test_proforma_excluded(self):
#         self.assertEqual(self.proformaTransaction.liquidated, None)


# class Converted(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=100)
#         self.convertible = ConvertibleSecurity(
#             is_converted=True,
#             converted_date=one_year_ago)
#         self.convertibleTransaction = TransactionFactory(
#             security=self.convertible,
#             date=two_years_ago,
#             debt=90)

#     def test_upgraded_convertibles(self):
#         self.assertEqual(self.convertibleTransaction.accrued, 99)


# class Proforma(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=100)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=100)

#     def test_proforma_simple(self):
#         self.assertEqual(self.commonTransaction.security.company.proforma(100, 400), (
#             {'new_money_shares': 50,
#                 'new_prorata_shares': 0,
#                 'new_converted_shares': 0,
#                 'new_investor_shares': 50,
#                 'new_pool_shares': 0,
#                 'price': 2}))


# class ProformaOption(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=500,
#             cash=5)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=500,
#             cash=500)
#         self.optionTransaction = TransactionFactory(
#             security=OptionSecurity(),
#             rights=100)

#     def test_proforma_option(self):
#         self.assertEqual(self.commonTransaction.security.company.proforma(200, 600), (
#             {'new_money_shares': 400.0,
#                 'new_prorata_shares': 0,
#                 'new_converted_shares': 0.0,
#                 'new_investor_shares': 400.0,
#                 'new_pool_shares': 0,
#                 'price': .5}))


# class ProformaPoolIncrease(TestCase):

#     def setUp(self):
#         self.commonTransaction = TransactionFactory(
#             security=CommonSecurity(),
#             shares=500)
#         self.preferredTransaction = TransactionFactory(
#             security=PreferredSecurity(),
#             shares=500)
#         self.optionTransaction = TransactionFactory(
#             security=OptionSecurity(),
#             rights=100)

#     def test_proforma_option(self):
#         pro = self.commonTransaction.security.company.proforma(200, 600, .1)
#         self.assertEqual(int(pro['new_money_shares']), 423)
#         self.assertEqual(int(pro['new_investor_shares']), 423)
#         self.assertEqual(int(pro['new_pool_shares']), 69)


# class TestOptionPoolZero(TestCase):

#     def setUp(self):

#         self.optionPool = OptionSecurity(
#             addition__authorized=1000)

#     def test_zero_granted(self):
#         """Tests that if there is an option pool ``granted`` returns 0"""
#         self.assertEqual(self.optionPool.company.granted, 0)
