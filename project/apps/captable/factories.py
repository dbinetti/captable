
import factory

import datetime

from django.utils.text import slugify

from .constants import *

from .models import (
    Company,
    Investor,
    Shareholder,
    Security,
    Addition,
    Certificate)


class CompanyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Company
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Test Company"
    slug = slugify(unicode(name))


class InvestorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Investor
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Test Investor"
    slug = slugify(unicode(name))


class ShareholderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Shareholder
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = "Test Shareholder"
    slug = slugify(unicode(name))
    investor = factory.SubFactory(InvestorFactory)


class AdditionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Addition
    FACTORY_DJANGO_GET_OR_CREATE = ('security',)

    date = datetime.date.today()
    authorized = 1000


class SecurityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Security
    FACTORY_DJANGO_GET_OR_CREATE = ('name', 'company')

    name = "Test Security"
    slug = slugify(unicode(name))
    date = datetime.date.today()
    security_type = SECURITY_TYPE_COMMON
    seniority = 1
    company = factory.SubFactory(CompanyFactory)
    addition = factory.RelatedFactory(AdditionFactory, 'security')


class CertificateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Certificate

    name = factory.Sequence(lambda n: 'CERT-{num}'.format(num=n))
    slug = slugify(unicode(name))
    date = datetime.date.today()
    shares = 1000
    shareholder = factory.SubFactory(ShareholderFactory)
    security = factory.SubFactory(SecurityFactory)
    vesting_start = datetime.date.today()
    vesting_term = 4.0
    vesting_cliff = 1.0
    vesting_immediate = 0.0


# class TransactionFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = Transaction

#     date = datetime.date.today()
#     shareholder = factory.SubFactory(ShareholderFactory)
#     security = factory.SubFactory(SecurityFactory)
#     vesting_start = datetime.date.today()
#     vesting_term = 4.0
#     vesting_cliff = 1.0
#     vesting_immediate = 0.0

# Security Factories
# #####################


class CommonSecurity(SecurityFactory):
    name = "Test Common"
    security_type = SECURITY_TYPE_COMMON
    seniority = 1


class PreferredSecurity(SecurityFactory):
    name = "Test Preferred"
    security_type = SECURITY_TYPE_PREFERRED
    price_per_share = 1
    liquidation_preference = 1
    is_participating = False
    participation_cap = 0.0
    conversion_ratio = 1
    seniority = 2


class ConvertibleSecurity(SecurityFactory):
    name = "Test Convertible"
    security_type = SECURITY_TYPE_CONVERTIBLE
    default_conversion_price = .1
    discount_rate = .1
    interest_rate = .1
    is_converted = False
    price_cap = 1000000
    seniority = 2


class OptionSecurity(SecurityFactory):
    name = "Test Option"
    security_type = SECURITY_TYPE_OPTION
    seniority = 1
    addition = factory.RelatedFactory(AdditionFactory, 'security', authorized=200)


class WarrantSecurity(SecurityFactory):
    name = "Test Warrant"
    security_type = SECURITY_TYPE_WARRANT
