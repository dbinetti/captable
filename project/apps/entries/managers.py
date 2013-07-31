from django.db import models
from django.db.models import Sum, Max
from django.db.models import get_model
from django.db.models.query import QuerySet

from constants import *



class SecurityQuerySet(QuerySet):
    def authorized(self):
        return self.aggregate(t=Sum('addition__authorized'))['t']


class CertificateQuerySet(QuerySet):
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
    def granted(self):
        """Calculates the total number of granted options.

        We need to differentiate between the concept of granted and
        extended because options that have been granted and exercised
        (either due to early exercise or normal exercise) are still counted
        against the total available option pool.  Meaning: the number
        of available options does not increase simply because those options
        have turned into shares.  The total number of options in the pool has
        a fixed limit to avoid inadvertent dilution"""

        certificates = self.select_related().filter(
            security__security_type=SECURITY_TYPE_OPTION).aggregate(
                t=Sum('granted'))['t']
        return certificates

    @property
    def exercised(self):
        """Calculates the total amount of exercised options"""
        certificates = self.select_related().filter(
            security__security_type=SECURITY_TYPE_OPTION).aggregate(
                t=Sum('exercised'))['t']
        return certificates

    @property
    def cancelled(self):
        """Calculates the granted but not exercised (ie, outstanding) options"""
        certificates = self.select_related().filter(
            security__security_type=SECURITY_TYPE_OPTION).aggregate(
                t=Sum('cancelled'))['t']
        return certificates

    @property
    def outstanding_options(self):
        """Calculates the granted but not exercised (ie, outstanding) options"""
        # TODO Normally this would be called 'outstanding', but that is
        # an overloaded term.
        if self.granted:
            return self.granted - self.exercised - self.cancelled
        else:
            return 0

    @property
    def warrants(self):
        """Calculates total warrants issued"""
        certificates = self.select_related()
        warrants = sum(filter(
            None, [c.outstanding_warrants for c in certificates]))
        if warrants:
            return warrants
        else:
            return 0

    @property
    def available(self):
        pool = self.select_related().filter(
            security__security_type=SECURITY_TYPE_OPTION).aggregate(
                t=Sum('security__addition__authorized'))['t']
        return pool - self.granted + self.cancelled


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


