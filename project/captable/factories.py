from .models import (
    Company,
    Investor,
    Shareholder,
    Transaction,
    Security,
    Addition,
    Certificate)

import factory

import datetime

from .constants import *


class CompanyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Company
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Default Company"


class InvestorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Investor
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Default Investor"


class ShareholderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Shareholder
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Default Shareholder"
    investor = factory.SubFactory(InvestorFactory)


class AdditionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Addition
    FACTORY_DJANGO_GET_OR_CREATE = ('security',)

    date = datetime.date.today()
    authorized = 1000


class SecurityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Security
    FACTORY_DJANGO_GET_OR_CREATE = ('name', 'company')

    name = "Default Security"
    date = datetime.date.today()
    security_type = SECURITY_TYPE_COMMON
    seniority = 1
    company = factory.SubFactory(CompanyFactory)
    addition = factory.RelatedFactory(AdditionFactory, 'security')


class TransactionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Transaction

    date = datetime.date.today()
    shareholder = factory.SubFactory(ShareholderFactory)
    security = factory.SubFactory(SecurityFactory)
    vesting_start = datetime.date.today()
    vesting_term = 4.0
    vesting_cliff = 1.0
    vesting_immediate = 0.0

# Security Factories
# #####################


class CommonSecurity(SecurityFactory):
    name = "Common Security"
    security_type = SECURITY_TYPE_COMMON
    seniority = 1


class PreferredSecurity(SecurityFactory):
    name = "Preferred Security"
    security_type = SECURITY_TYPE_PREFERRED
    price_per_share = 1
    liquidation_preference = 1
    is_participating = False
    participation_cap = 0.0
    conversion_ratio = 1
    seniority = 2



class ConvertibleSecurity(SecurityFactory):
    name = "Convertible Security"
    security_type = SECURITY_TYPE_CONVERTIBLE
    default_conversion_price = .1
    discount_rate = .1
    interest_rate = .1
    is_converted = False
    price_cap = 1000000
    seniority = 2


class OptionSecurity(SecurityFactory):
    name = "Option Security"
    security_type = SECURITY_TYPE_OPTION
    seniority = 1
    addition = factory.RelatedFactory(AdditionFactory, 'security', authorized=200)


class WarrantSecurity(SecurityFactory):
    name = "Warrant Security"
    security_type = SECURITY_TYPE_WARRANT
