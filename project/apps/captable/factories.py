
import factory

import datetime

from django.utils.text import slugify

from .constants import *

from .models import (
    Investor,
    Shareholder,
    Security,
    Addition,
    Certificate)

class InvestorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Investor
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    name = factory.Sequence(lambda n: unicode('Test Investor {0}').format(n))
    slug = factory.LazyAttribute(lambda a: slugify(unicode(a.name)))


class ShareholderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Shareholder
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = factory.Sequence(lambda n: unicode('Test Shareholder {0}').format(n))
    investor = factory.SubFactory(InvestorFactory)


class SecurityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Security
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    name = factory.Sequence(lambda n: 'Test Security {0}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(unicode(a.name)))
    date = datetime.date.today()
    security_type = SECURITY_TYPE_COMMON
    seniority = 1


class AdditionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Addition

    date = datetime.date.today()
    authorized = 100000000
    security = factory.SubFactory(SecurityFactory)


class CertificateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Certificate

    name = factory.Sequence(lambda n: 'CERT-{0}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(unicode(a.name)))
    date = datetime.date.today()
    shares = 10000
    shareholder = factory.SubFactory(ShareholderFactory)
    security = factory.SubFactory(SecurityFactory)
    vesting_start = datetime.date.today()
    vesting_term = 4.0
    vesting_cliff = 1.0
    vesting_immediate = 0.0



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
    price_per_share = .1
    discount_rate = .1
    interest_rate = .1
    price_cap = 1000000
    seniority = 2


class OptionSecurity(SecurityFactory):
    name = "Test Option"
    security_type = SECURITY_TYPE_OPTION
    seniority = 1


class WarrantSecurity(SecurityFactory):
    name = "Test Warrant"
    security_type = SECURITY_TYPE_WARRANT
