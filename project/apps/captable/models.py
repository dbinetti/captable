from __future__ import division

import datetime

from django.db import models
from django.db.models import Sum, Max
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.conf import settings

from django.utils.text import slugify

from model_utils.managers import PassThroughManager

from .constants import *

from .managers import (
    SecurityQuerySet,
    CertificateQuerySet,
    share_price,
    proforma as proforma2
)

class Investor(models.Model):
    """Investor represents the entity making the decision to invest.

    Examples of investors are VC firms, angels, banks, note holders,
    friends, family and fools.
    """

    name = models.CharField(max_length=200, help_text="""
        The name of the investor, which may be the same as the shareholder
        name.  For VCs, this would be the name of the VC firm itself.""")
    slug = models.SlugField(unique=True, help_text="""
        The slug is the slugified version of the investor name, is unique,
        and is used in composing the URL for the investor.""")
    contact = models.CharField(max_length=200, blank=True, help_text="""
        If the investor is a professional firm, the contact is the name
        to whom correspondance at the firm should be directed.""")
    address = models.CharField(max_length=200, blank=True, help_text="""
        The street address of the investor.""")
    city = models.CharField(max_length=200, blank=True, help_text="""
        The mailing city of the investor.""")
    state = models.CharField(max_length=2, blank=True, help_text="""
        The mailing state (two-letter abbreviation) of the investor.""")
    zipcode = models.CharField(max_length=20, blank=True, help_text="""
        The mailing zipcode of the investor.""")
    notes = models.TextField(blank=True, help_text="""
        A free-form notes field added for convenience.""")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Investor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('investor_detail', args=[str(self.slug)])

    def proceeds(self, purchase_price):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.proceeds(purchase_price) for c in certificates]))

    @property
    def liquidated(self):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.liquidated for c in certificates]))

    @property
    def outstanding(self):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.outstanding for c in certificates]))

    @property
    def paid(self):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.paid for c in certificates]))

    @property
    def principal(self):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.principal for c in certificates]))

    @property
    def preference(self):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.preference for c in certificates]))

    def proceeds_rata(self, purchase_price):
        proceeds = self.proceeds(purchase_price)
        total = Certificate.objects.select_related().proceeds(purchase_price)
        return proceeds / total

    def prorata(self, new_shares):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.prorata(new_shares) for c in certificates]))

    def exchanged(self, pre_valuation, price):
        certificates = Certificate.objects.filter(
            shareholder__investor=self)
        return sum(filter(None, [c.exchanged(pre_valuation, price) for c in certificates]))


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
    slug = models.SlugField(unique=True, help_text="""
        The slug is the slugified version of the investor name, is unique,
        and is used in composing the URL for the investor.""")
    investor = models.ForeignKey(Investor, help_text="""
        Every shareholder must a parent Investor.""")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Shareholder, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shareholder_detail', args=[str(self.slug)])


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
            (SECURITY_TYPE_PREFERRED, 'Preferred'),
            )
        ),
        ('Debt', (
            (SECURITY_TYPE_CONVERTIBLE, 'Convertible'),
            )
        ),
        ('Rights', (
            (SECURITY_TYPE_OPTION, 'Option'),
            (SECURITY_TYPE_WARRANT, 'Warrant'),
            )
        ),
    )

    name = models.CharField(max_length=50, help_text="""
        The name of the round of funding.
        Usual names are Common Stock, Series A, Series Seed, Founder Stock,
        Bridge Loan, Option Round A, Bridge Warrants, Convertible,
        or any other way to which the security is commonly referred.""")
    slug = models.SlugField(unique=True, help_text="""
        The slug is automatically generated based on the security name,
        which you can overwrite.""")
    date = models.DateField(default=datetime.date.today, help_text="""
        The date the security was created by the board.""")
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
        than 1:1.  The conversion ratio represents that conversion factor.  If
        a convertible, this should also be set to the conversion ratio of the
        security into which the convertible defaults under change of control.""")
    liquidation_preference = models.FloatField(blank=True, null=True, help_text="""
        In a liquidation preferred shares may receive proceeds differently
        than common shares.  The most common of these 'preferences' is the
        liquidation preference, which ensures that the preferred stock is
        paid before common stock in a company sale.  This variable represents
        the factor of initial principal to be returned before common is paid.
        1 X is typical.  NOTE: While convertibles do not
        have a direct liquidation preference, they will adopt the preference of
        the security into which they convert.  Therefore, be sure to add that
        preference here for convertibles as well.  If you can not determine
        what that preference will be in a default liquidation because it is
        not codified, then get that squared away with your investors immediately.""")
    is_participating = models.BooleanField(help_text="""
        If true, the peferred security participates along with common stock
        in addition to the liqudation preference.""")
    participation_cap = models.FloatField(blank=True, null=True, help_text="""
        If 'is participating' is true, refers to the cap participation in
        liquidation.  Set this to zero for a fully participating security.""")
    price_per_share = models.FloatField(blank=True, null=True, help_text="""
        For equity, this is the actual price-per-share paid as
        indicated on the term sheet (or from the proforma.)  For rights
        (ie, options and warrants) this is the strike price at which the
        underlying security may be purchased.  For convertible debt, this
        represents the default price at which the convertible will be
        exchanged if there is a change of control before a financing event. """)
    price_cap = models.IntegerField(blank=True, null=True, help_text="""
        Specific to convertible notes: the valuation cap from which a price per
        share will be derived at conversion (at the next round of financing.)""")
    discount_rate = models.FloatField(blank=True, null=True, help_text="""
        Specific to convertible notes: the discount rate at which the debt will covert
        assuming that there is no price-cap or the price cap is not met.""")
    interest_rate = models.FloatField(blank=True, null=True, help_text="""
        Specific to debt, the interest rate of the loan (assumed to be simple interest.)""")
    # default_conversion_price = models.FloatField(blank=True, null=True, help_text="""
    #     Specific to debt, the default conversion price of the debt if there is a
    #     change of control before a financing event.""")
    pre = models.FloatField(blank=True, null=True, help_text="""
        The pre-money valuation of the round.  If a convertible debt instrument,
        the pre-money valuation of the default instrument into which the debt will
        convert (usually that of the most recent equity round.)""")
    notes = models.TextField(blank=True, help_text="""
        A free-form notes field.""")
    seniority = models.IntegerField(blank=True, default=1, help_text="""
        Securities liquidate in a paricular order when the company exits.  This
        indicates the sequence of liquidation, with a higher number
        representing more senior security.  Common stock typically is
        liquidated last, and has a seniority of '1' (the default seniority.)""")
    # conversion_security = models.ForeignKey('self', blank=True, null=True, help_text="""
    #     The security into which this security converts.  This is often
    #     not yet known; if so do not enter anything here.""")

    objects = PassThroughManager.for_queryset_class(SecurityQuerySet)()

    class Meta:
        verbose_name_plural = "Securities"
        ordering = ['date']

    def __unicode__(self):
        return "{security}".format(
            security=self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Security, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('security_detail', args=[str(self.slug)])

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
            return u'Equity'
        elif self.security_type in [SECURITY_TYPE_CONVERTIBLE]:
            return u'Debt'
        elif self.security_type in [SECURITY_TYPE_OPTION]:
            return u'Options'

    @property
    def authorized(self):
        return Addition.objects.select_related().filter(
            security=self).aggregate(t=Sum('authorized'))['t']

    @property
    def available(self):
        return self.authorized - self.outstanding

    @property
    def outstanding(self):
        return Certificate.objects.select_related().filter(
            security=self).outstanding

    @property
    def outstanding_rata(self):
        outstanding = self.outstanding
        total = Certificate.objects.select_related().outstanding
        return outstanding / total

    @property
    def converted(self):
        return Certificate.objects.select_related().filter(
            security=self).converted

    @property
    def converted_rata(self):
        converted = self.converted
        total = Certificate.objects.select_related().converted
        return converted / total

    @property
    def diluted(self):
        if self.security_type == SECURITY_TYPE_OPTION:
            return Addition.objects.select_related().filter(
                security=self).aggregate(t=Sum('authorized'))['t']
        else:
            return Certificate.objects.select_related().filter(
                security=self).diluted

    @property
    def diluted_rata(self):
        diluted = self.diluted
        certs = Certificate.objects.select_related().diluted
        avail = Addition.objects.select_related().filter(
            security__security_type=SECURITY_TYPE_OPTION).aggregate(
                t=Sum('authorized'))['t']
        total = sum(filter(None, [certs, avail]))
        return diluted / total


class Addition(models.Model):
    """Addition represents changes in the amount of securities offered.

    Periodically the authorized amount of a given security may change as determined
    by the Board.  The most typical of these cases entails an increase
    in the number of available options which can be distributed according
    to a specific option plan (ie, an instance of a Security.)  This model
    allows for the total authorized sum of each Security to fluctutate
    through time as needed by the board.
    """
    date = models.DateField(default=datetime.date.today, help_text="""
        The date the additional shares/options were added to the security.""")
    authorized = models.IntegerField(blank=True, null=True, help_text="""
        This is the number of new shares/options added to the authorized
        number of shares available to the security itself.""")
    notes = models.TextField(blank=True, help_text="""
        A free-form notes field included for convenience.""")
    security = models.ForeignKey(Security, blank=True, null=True, help_text="""
        The underlying security to which the addition applies.""")

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return "{authorized:,} of {security} on {date}".format(
            authorized=self.authorized,
            security=self.security,
            date=self.date)


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
    slug = models.SlugField(unique=True, help_text="""
        The slug forms the URL at which this certificate may be accessed.
        It is automatically generated, but can be overwritten heres.""")
    date = models.DateField(default=datetime.date.today, help_text="""
        The date when the certificate was issued.""")
    shares = models.FloatField(default=0, help_text="""
        The shares of the transction, as expressed by the
        number of shares issued.""")
    returned = models.FloatField(default=0, help_text="""
        Shares can be repurchased (usually due to unvested portions
        being returned due to termination, etc.).  Enter any repurchased
        shares here, and include any corresponding refunds to the shareholder
        in the refunded box below""")
    cash = models.FloatField(default=0, help_text="""
        The cash paid for the transaction.  This will reflect the
        total purchase price for the shares.""")
    refunded = models.FloatField(default=0, help_text="""
        Enter any refunded amounts related to a repurchase here.""")
    is_prorata = models.BooleanField(default=False, help_text="""
        Preferred investors are often granted rights to purchase into a
        subsequent investment round according to their current rata position.
        If this investor (through the certificate) chooses to exercise
        prorata rights enter that here; the data will be used to make the
        appropriate calculations in the financing worksheets.""")

    principal = models.FloatField(default=0, help_text="""
        The original amount of debt issued (meaning, the actual
        cash amount, not any interest/accrued value.) """)
    forgiven = models.FloatField(default=0, help_text="""
        We do not want to lose information about any original debt instrument,
        so enter any forgiven/repaid principal here.  (Example: if the
        convertible converts, enter in the entire principal amount here
        to reflect that the loan has fully converted and there is no
        remaning debt obligation.""")

    granted = models.FloatField(default=0, help_text="""
        Enter the total number of options/warrants granted here.""")
    exercised = models.FloatField(default=0, help_text="""
        Options and warrants can be exercised in whole or in parts, either
        as they vest or due to early exercise.  Enter the exercised portion
        here.  (You may also wish to enter notes about each exercise in the
        notes field below.  I'm considering a feature where this can be tracked
        automatically, but currently that is not the case.""")
    cancelled = models.FloatField(default=0, help_text="""
        The unexercised/unvested portions of options and warrants can be
        cancelled/returned to the company.  Enter that number here.  The sum
        of the cancelled and exercised portion should not exceed the total
        amount granted.""")
    notes = models.TextField(blank=True, help_text="""
        Additional notes about the certificate.""")

    is_approved = models.BooleanField(default=False, help_text="""
        Grant transaction which has been approved by the board.  Options are
        often promised before they are officially granted; this boolean allows
        tracking of the promises to sure the option pool is not exceeded.  Set
        this to true when the options are officially sanctioned by the board.""")
    # is_vested = models.BooleanField(default=False, help_text="""
        # Transaction is fully vested""")
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

    security = models.ForeignKey(Security, help_text="""
        The underlying security of the certificate.""")
    shareholder = models.ForeignKey(Shareholder, help_text="""
        The legal owner of the certificate.  Enter a new shareholder from
        the Investor form before entering the certificate.""")

    objects = PassThroughManager.for_queryset_class(CertificateQuerySet)()

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Certificate, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{certificate} - {shareholder}'.format(
            certificate=self.name, shareholder=self.shareholder.name)

    def get_absolute_url(self):
        return reverse('certificate_detail', args=[str(self.slug)])


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

        # Preferred stock doesn't vest, as it is used by investors.
        if self.security.security_type == SECURITY_TYPE_PREFERRED:
            return self.outstanding

        # Convertibles don't vest, but they do convert at the default price
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
            return self.outstanding / self.security.price_per_share

        else:
            # Rights and shares are essentially equivalent in the vested
            # context; this simply assigns them for convenience.
            if self.security.security_type == SECURITY_TYPE_COMMON:
                stake = self.outstanding
            elif self.security.security_type == SECURITY_TYPE_WARRANT:
                stake = self.outstanding
            else:
                stake = self.outstanding

            # A "Single Trigger" is a provision in an agreement which
            # stipulates that all securities immediately vest in full
            # upon a change of control.  It is rare to grant single-
            # tiggers; a double-trigger is more common for founders/key
            # executives.  Normal employees generally don't get trigger
            # provisions at all.
            if self.vesting_trigger == TRIGGER_SINGLE:
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
            return 0

    @property
    def outstanding_warrants(self):
        if self.security.security_type in [SECURITY_TYPE_WARRANT]:
            return self.granted - self.cancelled - self.exercised
        else:
            return 0

    @property
    def outstanding_options(self):
        if self.security.security_type in [SECURITY_TYPE_OPTION]:
            return self.granted - self.cancelled - self.exercised
        else:
            return 0

    # @property
    # def outstanding_debt(self):
    #     if self.security.security_type in [SECURITY_TYPE_CONVERTIBLE]:
    #         return self.accrued - self.forgiven
    #     else:
    #         return 0

    @property
    def outstanding(self):
        if self.security.security_type in [
                SECURITY_TYPE_COMMON,
                SECURITY_TYPE_PREFERRED]:
            return self.shares - self.returned
        elif self.security.security_type in [SECURITY_TYPE_WARRANT]:
            return self.granted - self.cancelled - self.exercised
        elif self.security.security_type in [SECURITY_TYPE_OPTION]:
            return self.granted - self.cancelled - self.exercised
        # elif self.security.security_type in [SECURITY_TYPE_CONVERTIBLE]:
        #     return self.accrued - self.forgiven
        else:
            return 0



    @property
    def paid(self):
        if self.security.security_type in [
            SECURITY_TYPE_COMMON,
            SECURITY_TYPE_PREFERRED,
            SECURITY_TYPE_WARRANT]:
            return self.cash - self.refunded
        elif self.security.security_type in [
            SECURITY_TYPE_CONVERTIBLE]:
            return self.principal - self.forgiven
        else:
            return 0

    @property
    def converted(self):
        """Calculate the number of shares on an ``as converted`` basis.

        All securities have the potential to eventually become
        shares of common stock.  This function takes the transaction
        and produces the number of shares of common stock it represents
        on a "as converted" basis.  This result is used directly in the
        liquidation analysis, and is also used in calculating the
        fully-diluted share price, the demoninator of which assumes
        all securities convert to common.
        """
        # Preferred stock converts into a multiple of common stock.
        if self.security.security_type == SECURITY_TYPE_PREFERRED:
            return self.outstanding_shares * self.security.conversion_ratio

        # The as-converted number assumes the default price,
        # so use the ``exchanged`` function
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
            return self.exchanged()

        # Converted assumes all rights are exercised fully,
        # even the unvested portion
        # TODO: this should included vested
        elif self.security.security_type in [
                SECURITY_TYPE_OPTION,
                SECURITY_TYPE_WARRANT]:
            # return self.granted - self.cancelled - self.exercised
            return 0

        # All that remains is common stock, which
        # by definition requires no conversion.
        else:
            return self.outstanding_shares

    @property
    def diluted(self):
        """Calculate the number of shares on an ``fully diluted`` basis.

        All securities have the potential to eventually become
        shares of common stock.  This function takes the transaction
        and produces the number of shares of common stock it represents
        if all the possible issues that could be distributed and exercised
        were distributed and exercised.
        """
        # Preferred stock converts into a multiple of common stock.
        if self.security.security_type == SECURITY_TYPE_PREFERRED:
            return self.outstanding_shares * self.security.conversion_ratio

        # The as-converted number assumes the default price,
        # so use the ``exchanged`` function
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
            return self.exchanged()

        # Converted assumes all rights are exercised fully,
        # even the unvested portion
        # TODO: the difference here from converted should be one of VESTING
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
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE:
            return self.exchanged()
        elif self.security.security_type == SECURITY_TYPE_WARRANT:
            return self.granted
        else:
            return self.vested

    def discounted_price(self, pre_valuation=None, price=None):
        if self.security.security_type in [SECURITY_TYPE_PREFERRED,
            SECURITY_TYPE_COMMON] and self.cash and self.shares:
            return self.cash / self.shares
        elif self.security.security_type == SECURITY_TYPE_CONVERTIBLE and self.outstanding:
            return self.outstanding / self.exchanged(pre_valuation, price)
        else:
            return 0

    @property
    def preference(self):
        """Calculate the total preference of the transaction.

        Preferred stock is entitled to be paid in preference to common
        stock (hence the name 'preferred'.)  This function calculates
        the amount of the cash preference per the terms of the security.
        """
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
                return self.outstanding_debt * self.liquidation_preference
                # But if there is no parent then it reverts to the debt itself
                # This basically means that the preference is calling
                # the loan itself due and payable (with interest.)
            except:
                return self.accrued

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
            interest = self.principal * self.security.interest_rate * (
                (converted_date - self.date).days)/365
            return round(self.principal + interest, 2)

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
            return 0
        else:
            # Next we choose between the two conversion approaches

            # Choice A is the the value of the original loan in
            # equivalent dollars per the discount rate.
            discounted = self.accrued / (1-self.security.discount_rate)

            # Choice B is the value of the original loan in
            # equivalent dollars per the capped value in relation
            # to the pre-valuation
            if not pre_valuation:
                pre_valuation = self.security.pre
            capped = self.accrued * (pre_valuation/self.security.price_cap)

            # Then, simply pick whichever approach is best and return that.
            return max(discounted, capped)


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
            return 0
        elif pre_valuation:
            # Get the discounted value according to that method,
            # and divide by the price to calculate the number of shares.
            return self.discounted(pre_valuation) / price
        else:
            # Use the accrued value divided by the default price.
            return self.accrued / self.security.price_per_share

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
            fully_diluted = Security.objects.diluted

            # Get the current rata
            current_rata = self.outstanding / fully_diluted

            # And apply it to the new offering.
            return current_rata * new_shares
        else:
            return 0

    def proceeds(self, purchase_price):
        """Calculate proceeds from transaction at given purchase price.

        Calculates the proceeds from a transaction given a particular purchase
        price.
        """
        if self.liquidated:  # Return the proceeds: vested shares times price.
            return self.liquidated * share_price(purchase_price)[self.security.seniority]
        else:
            return 0

