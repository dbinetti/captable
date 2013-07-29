from __future__ import division

import datetime

# from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Sum, Max
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.conf import settings

from .constants import *


# class Company(models.Model):
#     """Company represents the corporation for the capitalization.

#     Company is self-explanatory; there should be only one cap table
#     per company.
#     """
#     name = models.CharField(max_length=200, help_text="""
#         The name of your company.""")
#     slug = models.SlugField(unique=True, help_text="""
#         This will be automatically populated for you based on the company
#         name.  Feel free to overwrite, but the slug must be URL friendly.""")
#     owner = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)

#     @property
#     def outstanding_shares(self):
#         """Calculates the total of issued and outstanding_shares shares"""
#         return Certificate.objects.select_related().filter(
#             security__company=self).outstanding_shares

#     @property
#     def pool(self):
#         """Calculates the total number of authorized options."""
#         pool = self.security_set.filter(
#             security_type=SECURITY_TYPE_OPTION).aggregate(
#                 pool=Sum('addition__authorized'))['pool']
#         return pool

#     @property
#     def granted(self):
#         """Calculates the total number of granted options.

#         We need to differentiate between the concept of granted and
#         extended because options that have been granted and exercised
#         (either due to early exercise or normal exercise) are still counted
#         against the total available option pool.  Meaning: the number
#         of available options does not increase simply because those options
#         have turned into shares.  The total number of options in the pool has
#         a fixed limit to avoid inadvertent dilution"""

#         certificates = Certificate.objects.select_related().filter(
#             security__company=self,
#             security__security_type=SECURITY_TYPE_OPTION).aggregate(
#                 t=Sum('granted'))['t']
#         return certificates

#     @property
#     def exercised(self):
#         """Calculates the total amount of exercised options"""
#         certificates = Certificate.objects.select_related().filter(
#             security__company=self,
#             security__security_type=SECURITY_TYPE_OPTION).aggregate(
#                 t=Sum('exercised'))['t']
#         return certificates

#     @property
#     def cancelled(self):
#         """Calculates the granted but not exercised (ie, outstanding) options"""
#         certificates = Certificate.objects.select_related().filter(
#             security__company=self,
#             security__security_type=SECURITY_TYPE_OPTION).aggregate(
#                 t=Sum('cancelled'))['t']
#         return certificates

#     @property
#     def outstanding_options(self):
#         """Calculates the granted but not exercised (ie, outstanding) options"""
#         # TODO Normally this would be called 'outstanding', but that is
#         # an overloaded term.
#         if self.granted:
#             return self.granted - self.exercised - self.cancelled
#         else:
#             return 0

#     @property
#     def warrants(self):
#         """Calculates total warrants issued"""
#         certificates = Certificate.objects.select_related().filter(
#             security__company=self)
#         warrants = sum(filter(
#             None, [c.outstanding_warrants for c in certificates]))
#         if warrants:
#             return warrants
#         else:
#             return 0

#     @property
#     def available(self):
#         """Calculates the remaining options in the option pool."""
#         pool = self.pool
#         if pool:
#             return pool - self.granted + self.cancelled
#         else:
#             return 0

#     def exchanged(self, pre_valuation=None, price=None):
#         """Calculates shares created in default liquidation"""
#         return Certificate.objects.select_related().filter(
#             security__company=self).exchanged(pre_valuation, price)

#     @property
#     def converted(self):
#         return Certificate.objects.select_related().filter(
#             security__company=self).converted

#     @property
#     def vested(self):
#         """Calculates shares created in default liquidation"""
#         return Certificate.objects.select_related().filter(
#             security__company=self).vested

#     @property
#     def diluted(self):
#         """Calculated the total number of shares fully diluted.

#         The fully diluted total represents the absolute highest number
#         of shares in the event that all shares which could be issued
#         were in fact issued.  This means all preferred stock converts
#         with its conversion ratio, all debt converts at the default price,
#         all options and warrants are fully vested, and includes all options
#         that could be distributed from the remaining option pool.  The only
#         number not considered in fully diluted total are authorized but
#         not issued stock.  (This is the case because any stock issuance
#         must still be approved by the board, and thus this is not
#         considered fully dilutive.)
#         """
#         return sum(filter(None, [
#             self.converted,
#             self.available]))

#     @property
#     def available_rata(self):
#         """Calculates the available option pool rata"""
#         return self.available / self.diluted

#     @property
#     def enabled(self):
#         """Calcluate the equity that is distributable.

#         I'm running out of synonyms here, but basically this represents
#         everything except debt.  It is the total diluted shares without
#         considering any default convesion of convertibles.
#         """
#         return sum(filter(
#             None, [
#                 self.outstanding,
#                 self.outstanding_options,
#                 self.warrants,
#                 self.available]))

#     def price(self, purchase_price):
#         """Calculate the per-security purchase price in liquidation.

#         In the event of a liquidation different classes of stock are
#         treated differently.  This function produces the price of
#         each security per the terms under which it was offered.
#         """

#         # First, gather all the transactions for this company.
#         certificates = Certificate.objects.select_related().filter(
#             security__company=self.id)

#         # Set the intial values for the variables that will be used
#         # within the liquidation loop.
#         residual_cash = purchase_price
#         residual_shares = certificates.liquidated

#         # Initiate the output variable
#         price = {}

#         # Determine the priority of the most senior security.
#         x = Security.objects.select_related().filter(
#             company=self.id).aggregate(
#                 t=Max('seniority'))['t']

#         # We are now going to loop through all transactions, grouped
#         # and ordered by security
#         while x > 0:

#             # Determine the price per share of whatever is left at
#             # this point.  This number serves as the threshold for
#             # all of the conditional logic.
#             residual_price = residual_cash / residual_shares

#             # Now filter for all the transactions at this level of seniority.
#             tranch_transactions = certificates.filter(security__seniority=x)

#             # And set the number of shares and preference accordingly.
#             tranch_shares = tranch_transactions.liquidated
#             tranch_preference = tranch_transactions.preference

#             # We also need to check for participation, and set those
#             # variables for the conditional logic.
#             is_participating = False
#             for t in tranch_transactions:
#                 if t.security.is_participating:
#                     is_participating = True
#                     participation_cap = t.security.participation_cap
#                     break

#             # With the prep work done, it's time for the core algorthm.

#             # First we need to see if there's enough cash to cover the
#             # current group of securities.  If not, then we rata out
#             # whatever cash remains and stop distributing proceeds by
#             # zeroing the price for all reamining securities.
#             if tranch_preference > residual_cash:
#                 residual_price = residual_cash / tranch_shares
#                 price.update({x: residual_price})
#                 x -= 1
#                 while x > 0:
#                     price.update({x: 0.0})
#                     x -= 1
#                 break

#             # Next, we consider participation.
#             elif is_participating:

#                 # And check if there is a cap.
#                 if participation_cap:

#                     # If the capped price is less than the residual price,
#                     # the security will convert to common.
#                     if (tranch_preference * participation_cap) / tranch_shares < residual_price:
#                         while x > 0:
#                             price.update({x: residual_price})
#                             x -= 1
#                         break

#                     # If the price is below the cap then first set the preference,
#                     # add the remaining residual pro-rata up to the cap,
#                     # reduce the residual cash and shares accordingly,
#                     # decrement the counter to indicate this group is finished,
#                     # and send through the loop again to handle the remaining.
#                     else:
#                         part_price = sum([
#                             tranch_preference / tranch_shares,
#                             (residual_cash - tranch_preference) / residual_shares])
#                         residual_cash -= part_price * tranch_shares
#                         residual_shares -= tranch_shares
#                         price.update({x: part_price})
#                         x -= 1

#                 # If there is no cap then the security is fully
#                 # participating, which means it first takes the
#                 # preference and then the proceeds on top -- there
#                 # is no conversion because the investor can have
#                 # his cake and eat it too.  Avoid this term if you can.
#                 else:
#                     part_price = sum([
#                         tranch_preference / tranch_shares,
#                         (residual_cash - tranch_preference) / residual_shares])
#                     residual_cash -= tranch_preference
#                     price.update({x: part_price})
#                     x -= 1

#             # if the overall price per share, diluted, exceeds the preference then
#             # any preferred stock will convert to common, meaning
#             # that all stock in all remaining tranches will be distributed
#             # ratably.  We do need to check for the capped participation
#             # condition first: there are cases where it's best to take
#             # the capped participation preference rather than convert.
#             # Note: it is assumed that if the top-preference converts
#             # to common, then all subsequent securities convert to common.
#             # If this isn't the case then the lawyers probably weren't doing
#             # their job.
#             elif (tranch_preference / tranch_shares) < residual_price:
#                 while x > 0:
#                     price.update({x: residual_price})
#                     x -= 1
#                 break

#             # The final condition means there is enough cash to cover
#             # the preference, but not enough to convert to common.  So,
#             # give the current tranch the preference, reduce the number
#             # of shares and cash remaining by what was distributed,
#             # and send through the loop again.
#             else:
#                 price.update({x: tranch_preference / tranch_shares})
#                 residual_cash -= tranch_preference
#                 residual_shares -= tranch_shares
#                 x -= 1

#         return price

#     def proforma(self, new_money, pre_valuation, pool_rata):
#         """Calculate the price and share totals of a prospective financing.

#         This function returns the number and price of new shares created
#         as a result of a proposed financing.  Proposed financings require two
#         variables:  the new money and pre-valuation.  For financings, this is
#         generally called an "X on Y", where X represents the new cash and Y the
#         pre-valuation.  This function assumes the standard case that all
#         convertibles and options are "in the pre", meaning that they are
#         considered as part of the determination of the share price.
#         """

#         # The post valuation is simply the prevaluation plus the new cash.
#         post_valuation = pre_valuation + new_money

#         # First, calculate what the new investors will expect in terms of
#         # ownership after the financing has occured.
#         new_rata = new_money / post_valuation

#         # Calculate what the convertible investors will expect per the terms
#         # of their debt instrument.
#         discounted = Certificate.objects.filter(
#             security__company=self.id).exclude(
#                 status=STATUS_CONVERTED).discounted(pre_valuation)
#         convert_rata = discounted / post_valuation

#         # Add the available options for use in calculations and if
#         # there is no option pool set to zero.
#         if self.available:
#             available = self.available
#         else:
#             available = 0

#         # Calculate the existing rata of granted shares; the pool must
#         # be expanded by a concordimant amount to reach the desired
#         # pool rata.
#         pre_shares = self.outstanding_shares + self.outstanding_options + self.warrants

#         # Aggregate the rata and determine the total expansion of
#         # capital from the existing number of outstanding shares
#         # and available option pool.
#         combined_rata = new_rata + convert_rata + pool_rata
#         if pool_rata:
#             expansion = (combined_rata / (1-combined_rata)) * (pre_shares + 0)
#         else:
#             expansion = (combined_rata / (1-combined_rata)) * (pre_shares + available)

#         # Ratably distribute shares such that everyone gets
#         # what one expects to get.
#         new_money_shares = (new_rata / combined_rata) * expansion
#         new_converted_shares = (convert_rata / combined_rata) * expansion
#         if pool_rata:
#             new_pool_shares = expansion - new_money_shares - new_converted_shares - available
#         else:
#             new_pool_shares = 0

#         # The prorata are the rights that existing investors have to
#         # ratably buy into the next round should they wish to.  See
#         # additional explanation and some caveats in the prorata
#         # method below under the Transaction model.
#         new_prorata_shares = Certificate.objects.filter(
#             security__company=self.id).prorata(new_money_shares)
#         new_investor_shares = new_money_shares - new_prorata_shares

#         # Finally, calculate the price of the new offering.
#         new_price = new_money / new_money_shares

#         return {
#             'available': available,
#             'pre_shares': pre_shares,
#             'expansion': expansion,
#             'new_rata': new_rata,
#             'combined_rata': combined_rata,
#             'new_money_shares': new_money_shares,
#             'new_prorata_shares': new_prorata_shares,
#             'new_converted_shares': new_converted_shares,
#             'new_investor_shares': new_investor_shares,
#             'new_pool_shares': new_pool_shares,
#             'price': new_price,
#         }

#     def get_absolute_url(self):
#         return reverse('captable.views.company', args=[str(self.id)])

#     def __unicode__(self):
#         return self.name

#     class Meta:
#         ordering = ['name']
#         verbose_name_plural = "Companies"


class Investor(models.Model):
    """Investor represents the entity making the decision to invest.

    Examples of investors are VC firms, angels, banks, note holders,
    friends, family and fools.
    """

    name = models.CharField(max_length=200, help_text="""
        The name of the investor, which may be the same as the shareholder
        name.  For VCs, this would be the name of the VC firm itself.""")
    slug = models.SlugField(unique=True)
    contact = models.CharField(max_length=200, blank=True, help_text="""
        The name of the contact person at the firm.""")
    address = models.CharField(max_length=200, blank=True, help_text="""
        The address of the contact person at the firm.""")
    city = models.CharField(max_length=200, blank=True, help_text="""
        The city of the contact person at the firm.""")
    state = models.CharField(max_length=2, blank=True, help_text="""
        The state of the contact person at the firm.""")
    zipcode = models.CharField(max_length=20, blank=True, help_text="""
        The name of the contact person at the firm.""")

    def get_absolute_url(self):
        return reverse('captable.views.investor', args=[str(self.id)])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Shareholder(models.Model):
    """Shareholder is the legal entity which holds the security.

    Shareholder represents the legal entity which provides
    the actual fund source and is the legal owner.  In the case of a VC firm,
    this would be the fund (generally organized as a LP), or if
    an Angel could be represented by a trust or other financial vehicle.
    """
    name = models.CharField(max_length=200, help_text="""
        The legal name of the shareholder.  In the case of venture investment,
        this would be the formal, legal name of the fund.""")
    slug = models.SlugField(unique=True)
    investor = models.ForeignKey(Investor, help_text="""
        Every shareholder has a parent Investor.""")

    def get_absolute_url(self):
        return reverse('captable.views.shareholder', args=[str(self.id)])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Security(models.Model):
    """Security represents an specific financing instrument.

    A Security represents a specific financing instrument, and is usually
    accompanied by its own form of legal documentation.  Examples of
    securities include common stock, a Series A offering, a covertible
    loan, etc.  Securities can be similiar but have different terms,
    such as a Series A offering and a Series B offering, both of which
    are preferred stock but may have different prices or preferences.
    """

    SECURITY_TYPE = (
        ('Equity', (
            (SECURITY_TYPE_COMMON, 'Common'),
            (SECURITY_TYPE_PREFERRED, 'Preferred'))),
        ('Debt', (
            (SECURITY_TYPE_CONVERTIBLE, 'Convertible'),)),
        ('Rights', (
            (SECURITY_TYPE_OPTION, 'Option'),
            (SECURITY_TYPE_WARRANT, 'Warrant'),)),)

    name = models.CharField(max_length=50, help_text="""
        The name of the round of funding.
        Common names are Series A, Series Seed, Founder Stock,
        Bridge Loan, Option Round A, Bridge Warrants, Convertible,
        or any other way to which the round is commonly referred.""")
    slug = models.SlugField(help_text="""
        The slug is automatically generated based on the security name,
        which you can overwrite.""")
    date = models.DateField(default=datetime.date.today)
    security_type = models.IntegerField(max_length=20, choices=SECURITY_TYPE, help_text="""
        The specific type of the security issued.  Choices are:
        - Common Stock.  This stock is typically issued to founders and employees.
        - Preferred Stock.  This stock is typically issued to investors.
        - Convertible Debt.  This is a loan that converts to stock (usually preferred)
        - Options.  This is a right to purchase stock at a particular price.  Usually
                    granted to employees, and usually is for common stock.
        - Warrants. This is a right to purchased stock at a particuar price.  Usually
                    granted to investors, and is usually for preferred stock.""")
    conversion_ratio = models.FloatField(blank=True, null=True, help_text="""
        Preferred shares may convert into common shares at a factor other
        than 1:1.  The conversion ratio represents that conversion factor.""")
    liquidation_preference = models.FloatField(blank=True, null=True, help_text="""
        In a liquidation preferred shares may receive proceeds differently
        than common shares.  The most common of these 'preferences' is the
        liquidation preference, which ensures that the preferred stock is
        paid before common stock in a company sale.  This variable represents
        the factor of initial principal to be returned before common is paid.
        1 X is typical, so enter 1.0 here.""")
    is_participating = models.BooleanField(help_text="""
        If true, the peferred security participates along with common stock
        in addition to the liqudation preference.""")
    participation_cap = models.FloatField(blank=True, null=True, help_text="""
        If 'is participating' is true, refers to the cap participation in
        liquidation.  Set this to zero for a fully participating security.""")
    price_per_share = models.FloatField(blank=True, null=True, help_text="""
        The actual price-per-share paid as part of the term sheet.  This is a
        denormalization provided for convenience, and historical reference
        and to address any deviation from actual due to rounder error.""")
    price_cap = models.IntegerField(blank=True, null=True, help_text="""
        Specific to converible notes: the valuation cap set for the offering in
        total valuation terms, from which a price per share will be derived at conversion
        (at the next round of financing.)""")
    discount_rate = models.FloatField(blank=True, null=True, help_text="""
        Specific to convertible notes: the discount rate at which the debt will covert
        assuming that there is no price-cap or the price cap is not met.""")
    interest_rate = models.FloatField(blank=True, null=True, help_text="""
        Specific to debt, the interest rate of the loan (assumed to be simple interest.)""")
    default_conversion_price = models.FloatField(blank=True, null=True, help_text="""
        Specific to debt, the default conversion price upon change of control before conversion.""")
    pre = models.FloatField(blank=True, null=True, help_text="""
        The pre-money valuation.""")
    notes = models.TextField(blank=True)
    seniority = models.IntegerField(blank=True, default=1, help_text="""
        Securities liquidate in a paricular order when the company exits.  This
        indicates the sequence of liquidiation, with a higher number
        representing more senior security.  Common stock typically is
        liquidated last, and has a seniority of '1' (the default seniority.)""")
    # company = models.ForeignKey(Company, help_text="""
    #     The parent company to which this security belongs.""")
    conversion_security = models.ForeignKey('self', blank=True, null=True, help_text="""
        The security into which this security converts.  This is often
        not yet known; if so do not enter anything here.""")

    @property
    def security_class(self):
        """Determine the highest class of the security.

        Securites can take one of three forms:
        - Equity: Representing ownership in the company.
        - Debt: Representing a financial obligation but no ownership.
        - Rights: Representing a right to purchase equity, but is not
                  actual ownership.
        """
        if self.security_type in [SECURITY_TYPE_COMMON, SECURITY_TYPE_PREFERRED, SECURITY_TYPE_WARRANT]:
            return 'Equity'
        elif self.security_type in [SECURITY_TYPE_CONVERTIBLE]:
            return 'Debt'
        elif self.security_type in [SECURITY_TYPE_OPTION]:
            return 'Options'

    @property
    def authorized(self):
        authorized = Addition.objects.select_related().filter(
            security=self.id).aggregate(
                t=Sum('authorized'))['t']
        return authorized

    @property
    def outstanding_shares(self):
        return Certificate.objects.filter(
            security=self.id).outstanding_shares

    @property
    def converted(self):
        return Certificate.objects.filter(
            security=self.id).converted

    def exchanged(self, pre_valuation=None, price=None):
        return Certificate.objects.filter(
            security=self.id).exchanged(pre_valuation, price)

    def get_absolute_url(self):
        return reverse('captable.views.security', args=[str(self.id)])

    def __unicode__(self):
        return "{security}".format(
            security=self.name)

    class Meta:
        verbose_name_plural = "Securities"
        ordering = ['date']


class Addition(models.Model):
    """Addition represents changes in the amount of securities offered.

    Periodically the authorized amount of a given security may change as determined
    by the Board.  The most typical of these cases entails an increase
    in the number of available options which can be distributed according
    to a specific option plan (ie, an instance of a Security.)  This model
    allows for the total authorized sum of each Security to fluctutate
    through time as needed by the board.
    """
    date = models.DateField(default=datetime.date.today)
    authorized = models.IntegerField(blank=True, null=True, help_text="""
        This is the number of new shares added to the authorized number of
        shares available to the security itself.""")
    notes = models.TextField(blank=True, help_text="""
        A free-form notes field included for convenience.""")
    security = models.ForeignKey(Security, blank=True, null=True, help_text="""
        The underlying security to which the addition applies.""")

    def get_absolute_url(self):
        return reverse('captable.views.addition', args=[str(self.id)])

    def __unicode__(self):
        return "{authorized:,} of {security} on {date}".format(
            authorized=self.authorized,
            security=self.security,
            date=self.date)

    class Meta:
        ordering = ['date']


class CertificateMixin(object):

    @property
    def liquidated(self):
        """Calculates the as-converted share totals"""
        certificates = self.select_related()
        return sum(filter(
            None, [t.liquidated for t in certificates]))

    @property
    def preference(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.preference for t in certificates]))

    @property
    def paid(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.paid for t in certificates]))

    @property
    def outstanding_debt(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.outstanding_debt for t in certificates]))

    @property
    def converted(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.converted for t in certificates]))

    def discounted(self, pre_valuation=None):
        certificates = self.select_related()
        return sum(filter(
            None, [t.discounted(pre_valuation) for t in certificates]))

    def prorata(self, new_shares):
        certificates = self.select_related()
        return sum(filter(
            None, [t.prorata(new_shares) for t in certificates]))

    def exchanged(self, pre_valuation, price):
        certificates = self.select_related()
        return sum(filter(
            None, [t.exchanged(pre_valuation, price) for t in certificates]))

    @property
    def vested(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.vested for t in certificates]))

    @property
    def outstanding_shares(self):
        certificates = self.select_related()
        return sum(filter(
            None, [t.outstanding_shares for t in certificates]))

    def proceeds(self, purchase_price):
        certificates = self.select_related()
        return sum(filter(
            None, [t.proceeds(purchase_price) for t in certificates]))


class CertificateQuerySet(QuerySet, CertificateMixin):
    pass


class CertificateManager(models.Manager, CertificateMixin):
    def get_query_set(self):
        return CertificateQuerySet(self.model, using=self._db)


class Certificate(models.Model):
    """Certificate represents a specific record of ownership.

    The Certificate model represents the physical record of ownership,
    whether that is a stock certificate, promissory note, option aggreement,
    warrant, or other similar document.  It is the intersection of the
    Shareholder (the investor as owner) and the security (the portion of
    the company being offered as equity/debt/or other right of ownership.)
    """

    TRIGGER_CHOICES = (
        (TRIGGER_NONE, "No Trigger"),
        (TRIGGER_SINGLE, "Single Trigger"),
        (TRIGGER_DOUBLE, "Double Trigger"))

    STATUS_CHOICES = (
        (STATUS_OUTSTANDING, "Outstanding"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_TRANSFERRED, "Transferred"),
        (STATUS_EXERCISED, "Exercised"),
        (STATUS_CONVERTED, "Converted"),)

    name = models.CharField(max_length=200, help_text="""
        This is a unique name/serial number for the certificate.""")
    slug = models.SlugField(help_text="""
        The slug is automatically generated.""")
    date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUS_CHOICES, default=STATUS_OUTSTANDING)

    shares = models.FloatField(default=0, help_text="""
        The shares of the transction, as expressed by the
        number of shares purchased.""")
    returned = models.FloatField(default=0)
    cash = models.FloatField(default=0, help_text="""
        The cash paid for the transaction.  This will reflect the
        total purchase price for the shares, or the amount of debt issued.""")
    refunded = models.FloatField(default=0)
    debt = models.FloatField(default=0, help_text="""
        Debt """)
    forgiven = models.FloatField(default=0, help_text="""
        Forgiven debt.  Should equal cash in conversion.""")
    granted = models.FloatField(default=0, help_text="""
        The total amount of the original option/warrant grant.""")
    exercised = models.FloatField(default=0)
    cancelled = models.FloatField(default=0)

    notes = models.TextField(blank=True, help_text="""
        Additional notes about the certificate.""")

    is_prorata = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, help_text="""
        Grant transaction which has been approved by the board.  Options are
        often promised before they are officially granted; this boolean allows
        tracking of the promises to sure the option pool is not exceeded.  Set
        this to true when the options are officially sanctioned by the board.""")
    is_vested = models.BooleanField(default=False, help_text="""
        Transaction is fully vested""")
    vesting_start = models.DateField(blank=True, null=True, help_text="""
        The start date of the vesting""")
    vesting_stop = models.DateField(blank=True, null=True, help_text="""
        The date when vesting stopped (due to termination, etc.)""")
    vesting_term = models.FloatField(blank=True, null=True, help_text="""
        The overall period of time, in months, of the vesting period.""")
    vesting_cliff = models.FloatField(blank=True, null=True, help_text="""
        The duration of the vesting 'cliff', in months.  Cliff refers to the
        initial period of time before any shares are vested. Typically 1 year.""")
    vesting_immediate = models.FloatField(blank=True, null=True, help_text="""
        The percentage of the transaction which has immediately vested
        on the closing of the transaction itself.""")
    vested_direct = models.FloatField(blank=True, null=True, help_text="""
        If the vesting schedule is ad-hoc, enter vested shares here and set term to 0""")
    vesting_trigger = models.IntegerField(blank=True, null=True, choices=TRIGGER_CHOICES, help_text="""
        The trigger describes any accelerated vesting on change of control.""")
    expiration_date = models.DateField(blank=True, null=True, help_text="""
        The date on which the grant expires.""")
    converted_date = models.DateField(blank=True, null=True, help_text="""
        The date the certificate converted.""")
    security = models.ForeignKey(Security)
    shareholder = models.ForeignKey(Shareholder)
    objects = CertificateManager()

    @property
    def vested(self):
        """Calculates the vested shares.

        Stock which is granted to founders, employees, advisors and other
        non-investors typically vests over time.  This means that while
        the underlying security has technically be granted to the recipient,
        a portion of it is subject to repurchase according to a vesting
        schedule.  Vesting is a technique used to ensure the continued
        service of an employee of the company through time.  This
        method calcuates the number of shares vested in the underlying
        security given the terms of the original grant.

        This property is specifically used in the calculation of
        liquidation proceeds, which only considers vested shares.  Thus,
        the calculation for convertibles consideres the default
        conversion price, which occurs in a liquidation and is different
        than the number of shares converted in a financing.
        """

        # Proforma and converted transactions don't vest.
        if self.status != STATUS_OUTSTANDING:
            return 0

        # Preferred stock doesn't vest, as it is used by investors.
        elif self.security.security_type == SECURITY_TYPE_PREFERRED:
            return self.outstanding_shares

        # Convertibles don't vest, but they do convert at the default price
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
            return self.outstanding / self.security.default_conversion_price

        else:
            # Rights and shares are essentially equivalent in the vested
            # context; this simply assigns them for convenience.
            if self.security.security_type == SECURITY_TYPE_COMMON:
                stake = self.outstanding_shares
            elif self.security.security_type == SECURITY_TYPE_WARRANT:
                stake = self.outstanding_warrants
            else:
                stake = self.outstanding_options

            # A "Single Trigger" is a provision in an agreement which
            # stipulates that all securities immediately vest in full
            # upon a change of control.  It is rare to grant single-
            # tiggers; a double-trigger is more common for founders/key
            # executives.  Normal employees generally don't get trigger
            # provisions at all.
            if self.vesting_trigger == TRIGGER_SINGLE:
                return stake
            elif self.is_vested:
                return stake
            else:
                return stake

                # # TODO Need a way to handle ad-hoc vesting gracefully
                # if self.vesting_term:
                #     # Calculate the immediately vested portion.  Sometimes
                #     # founders receive a year vesting immediately as a
                #     # expression of "time served."  This also can be an
                #     # inducement for a key hire/advisor, etc.
                #     immediate = stake * self.vesting_immediate
                #     residual = stake - immediate

                #     # For the remaining, non-immediately vested portion,
                #     # calculate the number of months vesting
                #     months_vesting_period = self.vesting_term

                #     # If the vesting was halted due to termination, etc.,
                #     # use that date for the ending period.  Otherwise,
                #     # use today to calculate the total vesting period.
                #     if self.vesting_stop:
                #         vesting_stop = self.vesting_stop
                #     else:
                #         vesting_stop = datetime.date.today()

                #     # Now calculate the total number of months vested from
                #     # the start and the stop dates, in months.
                #     rd = relativedelta(vesting_stop, self.vesting_start)
                #     months_vested = rd.years * 12 + rd.months

                #     # Many grants will have a "cliff", meaning an initial
                #     # period before any grants will vest.  Determine the
                #     # cliff in terms of months.
                #     months_cliff = self.vesting_cliff

                #     # Grants are fully vested if all time has passed.
                #     if months_vested > months_vesting_period:
                #         residual_vested = residual
                #     # And nothing has vested if within the cliff
                #     elif months_vested < months_cliff:
                #         residual_vested = 0
                #     # Finally, calculate the rata portion of what ever
                #     # didn't immediately vest according to the amount of
                #     # time passed.
                #     else:
                #         monthly_vested = residual / months_vesting_period
                #         residual_vested = monthly_vested * months_vested
                #     return immediate + residual_vested
                # else:
                #     return self.vested_direct

    @property
    def outstanding_shares(self):
        """Defines current numbers"""
        if self.security.security_type in [
                SECURITY_TYPE_COMMON,
                SECURITY_TYPE_PREFERRED]:
            return self.shares - self.returned
        else:
            return None

    @property
    def outstanding_warrants(self):
        if self.security.security_type in [SECURITY_TYPE_WARRANT]:
            return self.granted - self.cancelled - self.exercised
        else:
            return None

    @property
    def outstanding_options(self):
        if self.security.security_type in [SECURITY_TYPE_OPTION]:
            return self.granted - self.cancelled - self.exercised
        else:
            return None

    @property
    def outstanding_debt(self):
        if self.security.security_type in [SECURITY_TYPE_CONVERTIBLE]:
            return self.accrued - self.forgiven
        else:
            return None

    @property
    def paid(self):
        return self.cash - self.refunded

    @property
    def converted(self):
        # TODO Change to diluted?
        """Calculate the number of shares on an ``as converted`` basis.

        All securities have the potential to eventually become
        shares of common stock.  This function takes the transaction
        and produces the number of shares of common stock it represents
        on a "as converted" basis.  This result is used directly in the
        liquidation analysis, and is also used in calculating the
        fully-diluted share price, the demoninator of which assumes
        all securities convert to common.
        """

        # Proforma and converted are not relevant.
        if self.status != STATUS_OUTSTANDING:
            return None
        else:

            # Preferred stock converts into a multiple of common stock.
            if self.security.security_type == SECURITY_TYPE_PREFERRED:
                return self.outstanding_shares * self.security.conversion_ratio

            # The as-converted number assumes the default price,
            # so use the ``exchanged`` function
            elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
                return self.exchanged()

            # Converted assumes all rights are exercised fully,
            # even the unvested portion
            elif self.security.security_type in [
                    SECURITY_TYPE_OPTION,
                    SECURITY_TYPE_WARRANT]:
                return self.granted - self.cancelled - self.exercised

            # All that remains is common stock, which
            # by definition requires no conversion.
            else:
                return self.outstanding_shares

    @property
    def liquidated(self):
        """Calculate the shares that would be liquidated in a liquidation.

        Redeemed is a shortcut method that simply calculates shares that
        would be liquidated in a liquidation at any given point in time.
        It would typically represent the number of shares "as converted"
        less the unallocated option pool and all unvested common stock/
        options.  All debt converts at the default conversion price.
        """

        if self.security.security_type == SECURITY_TYPE_PREFERRED:
            return self.shares * self.security.conversion_ratio
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE and self.status == STATUS_CONVERTED:
            return self.exchanged(self.security.conversion_security.pre, self.security.conversion_security.price_per_share)
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE and self.status != STATUS_CONVERTED:
            return self.exchanged()
        elif self.security.security_type == SECURITY_TYPE_WARRANT:
            return self.granted
        else:
            return self.vested

    @property
    def discounted_price(self):
        if self.cash and self.shares:
            return self.cash / self.shares
        else:
            return None

    @property
    def preference(self):
        """Calculate the total preference of the transaction.

        Preferred stock is entitled to be paid in preference to common
        stock (hence the name 'preferred'.)  This function calculates
        the amount of the cash preference per the terms of the security.
        """
        if self.status != STATUS_OUTSTANDING:
            return None
        else:

            # We use the ``price_per_share`` variable here since the
            # original investment vehicle may have been a convertible
            # and the original cash paid may not be relevant.
            # Note: this is an important concept which can affect future
            # financings.  The term is called "liquidation overhang"
            # and you should learn more about it.  Yokum Taku at WSGR
            # has proposed  solutions to avoid it and you should
            # read about them here:
            # http://www.startupcompanylawyer.com/category/convertible-note-bridge-financing/
            if self.security.security_type == SECURITY_TYPE_PREFERRED:
                return (
                    self.outstanding_shares
                    * self.security.price_per_share
                    * self.security.liquidation_preference)
            elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
                try:
                    # If the stock converts it will share the same preference
                    # as its parent security.
                    return self.outstanding_debt * self.security.conversion_security.liquidation_preference
                    # But if there is no parent then it reverts to the debt itself
                    # This basically means that the preference is calling
                    # the loan itself due and payable (with interest.)
                except:
                    return self.outstanding_debt

    @property
    def accrued(self):
        """Calculate the total accrued debt per the interest rate"""

        # Only debt accrues interest.
        if self.security.security_type == SECURITY_TYPE_CONVERTIBLE:

            # Calculate the interest and add to the principal.
            if self.converted_date:
                converted_date = self.converted_date
            else:
                converted_date = datetime.date.today()
            # Convertible debt interest is nearly always simple interest.
            interest = self.debt * self.security.interest_rate * (
                (converted_date - self.date).days)/365
            return round(self.debt + interest, 2)

        else:
            return None

    def discounted(self, pre_valuation=None):
        """Calculate the purchase power of a convertible.

        Convertibles convert into preferred stock according to the terms
        of the original note.  Typically this takes the form of
        A) a discount off of the purchase price, or
        B) a 'capped' price based on a specified pre-valuation.
        Each of these approaches represents a specific number in the
        purchase power of a given dollar of convertible debt.  For
        instance, $1 is worth $1.25, discounted 20%. [(1/(1-.2))=1.25].

        This function takes the existing convertible and
        returns the current value of the transaction in terms of the
        equivalent dollar value at which it can purchase the next round
        (or default conversion) of preferred stock.
        """
        if self.security.security_type != SECURITY_TYPE_CONVERTIBLE:
            return None

        else:
            # First we need to check if there is a financing event.
            if self.status == STATUS_CONVERTED:
                # Next we choose between the two conversion approaches

                # Choice A is the the value of the original loan in
                # equivalent dollars per the discount rate.
                discounted = self.outstanding_debt / (1-self.security.discount_rate)

                # Choice B is the value of the original loan in
                # equivalent dollars per the capped value in relation
                # to the pre-valuation
                pre_valuation = self.security.conversion_security.pre
                capped = self.outstanding_debt * (pre_valuation/self.security.price_cap)

                # Then, simply pick whichever approach is best and return that.
                return max(discounted, capped)
            # And if there isn't a financing event then
            # there is no discount to apply; simply return the accrued value.
            else:
                return self.outstanding

    def exchanged(self, pre_valuation=None, price=None):
        """Calculate the shares from a convertible note.

        Convertible debt is designed to convert into the next security
        offering as part of a financing.  Convertibles used to be called
        'bridge loans' specifically because there were typically only
        used in those transitional situations.  However, convertibles
        have become more popular as financing instruments in their own
        right, and there are often situations where there is no subsequent
        financing and the convertibles must convert in a liquidation.

        Typically there will be 'change of control' provisions written
        into the terms of the convertible, with the standard case being
        that they convert into the latest round of preferred stock at a
        predetermined default price.  This function returns what the
        convertible represents in shares under those considitions.
        Note: if your convertible terms do not include these provisions
        then get them added immediatley.  You don't want to get into
        legal wrangling over unclear terms in the event of a liquidation.
        It will be a huge hassle and you don't want to make a potential
        purchaser worried about the unknowns involved.

        Note holders will also often have the right to make their
        debt immediately due upon a change of control; use the accrued
        property to determine what that amount will be should they
        elect to do so.
        """
        #  Don't convert what can't be converted
        if self.security.security_type != SECURITY_TYPE_CONVERTIBLE:
            return None
        # elif self.status == STATUS_CONVERTED:
        #     return 0
        elif pre_valuation:
            # Get the discounted value according to that method,
            # and divide by the price to calculate the number of shares.
            return self.discounted(pre_valuation) / price
        else:
            # Use the accrued value divided by the default price.
            return self.outstanding / self.security.default_conversion_price

    def prorata(self, new_shares):
        """Return the Investor's prorata.

        Existing investors sometimes have the right to purchase shares
        of the next round of funding in an amount such that they can
        maintain their existing ownership percentage.  This is commonly
        referred to as the "prorata", or "ROFR" (right of first refusal).
        This funciton checks to see if the investor wishes to exercise
        his/her prorata, and then returns the number of shares to be
        purchased given the shares offered as part of a new financing.

        Prorata shares yypically comes from the total new money offering.
        Be careful on proratas, as new investors may require a certain
        minimum level of ownership to invest, which is necessarily reduced
        by any prorata elected by existing investors.  You may need to take
        more money that you would otherwise need to, resulting in higher
        dilution for you and your employees.
        """
        # Only preferred has prorata rights, and not every investor
        # may have or choose to exercise them.  Check that first.
        if self.is_prorata:

            # Calculation of the rata is done on a fully-diluted basis.
            # fully_diluted = self.security.company.diluted
            fully_diluted = 1000000

            # Get the current rata
            current_rata = self.outstanding_shares / fully_diluted

            # And apply it to the new offering.
            return current_rata * new_shares
        else:
            return None

    def proceeds(self, purchase_price):
        """Calculate proceeds from transaction at given purchase price.

        Calculates the proceeds from a transaction given a particular purchase
        price.
        """

        # Ignore the irrelevant.
        if self.status != STATUS_OUTSTANDING:
            return None
        else:
            if self.liquidated:  # Return the proceeds: vested shares times price.
                return self.liquidated * self.security.company.price(purchase_price)[self.security.seniority]
            else:
                return 0

    def __unicode__(self):
        return '{certificate} - {shareholder}'.format(
            certificate=self.name, shareholder=self.shareholder.name)

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    """Transactional notes related to a certificate.

    Originally this model served to track each atomic transaction.  For
    simplicity it has been downgraded to a logging field, where notes
    related to any changes in Certificate instances may be recorded.
    """

    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True)
    certificate = models.ForeignKey(Certificate, help_text="""
        The certificate to which this transaction is related.""")

    def get_absolute_url(self):
        return reverse('captable.views.transaction', args=[str(self.id)])

    def __unicode__(self):
        return '{certificate}'.format(
            certificate=self.certificate.name)

    class Meta:
        ordering = ['date']
