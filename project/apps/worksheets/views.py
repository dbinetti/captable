from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from constants import *

from apps.entries.models import (
    Transaction,
    Shareholder,
    Security,
    Investor,
    Certificate)

from .tables import (
    LiquidationTable,
    FinancingTable,
)

from .managers import (
    share_price,
    proforma as proforma2
)

# @login_required
def summary(request):
    """Renders the summary cap table."""

    securities = Security.objects.order_by('security_type', 'date')
    return render(
        request, 'summary.html', {'securities': securities})


# @login_required
# def financing(request, new_money, pre_valuation, pool_rata):
#     """Renders the financing table"""

#     new_money = float(new_money)
#     pre_valuation = float(pre_valuation)
#     pool_rata = float(pool_rata)/100

#     # get the objects needed for the page
#     investors = Investor.objects.select_related().filter(
#             shareholder__certificate__security__security_type__in=[
#                 SECURITY_TYPE_COMMON,
#                 SECURITY_TYPE_CONVERTIBLE,
#                 SECURITY_TYPE_PREFERRED])

#     certificates = Certificate.objects.select_related()

#     # get the proforma
#     proforma = certificates.proforma(new_money, pre_valuation, pool_rata)

#     # populate the variables
#     price = proforma['price']
#     new_investor_shares = proforma['new_investor_shares']
#     new_pool_shares = proforma['new_pool_shares']
#     new_money_shares = proforma['new_money_shares']
#     new_prorata_shares = proforma['new_prorata_shares']
#     new_converted_shares = proforma['new_converted_shares']
#     available = proforma['available']

#     # set the 'globals'
#     total_pre_shares = available + certificates.converted

#     total_pre_cash = certificates.paid

#     total_prorata_cash = new_prorata_shares * price
#     total_converted_cash = certificates.outstanding_debt

#     total_post_shares = sum([
#         total_pre_shares,
#         new_money_shares,
#         new_converted_shares,
#         new_pool_shares])

#     total_post_cash = sum(filter(
#         None, [total_pre_cash, new_money, total_converted_cash]))

#     # Instantiate the context
#     posts = []

#     # Create the New Investor row
#     new_investor_cash = new_money - total_prorata_cash
#     new_investor_rata = new_investor_shares / total_post_shares

#     total_pre_rata = 0
#     total_post_rata = new_investor_rata

#     posts.append({
#         'name': 'New Investor',
#         'pre_shares': '',
#         'pre_cash': '',
#         'pre_price': '',
#         'pre_rata': '',
#         'prorata_shares': '',
#         'prorata_cash': '',
#         'converted_shares': '',
#         'converted_cash': '',
#         'converted_price': '',
#         'post_shares': new_investor_shares,
#         'post_cash': new_investor_cash,
#         'post_price': price,
#         'post_rata': new_investor_rata

#     })

#     # Create the investor list
#     for i in investors:
#         investor_certs = certificates.filter(
#             shareholder__investor=i)
#         pre_shares = investor_certs.outstanding_shares
#         if pre_shares == 0:
#             continue
#         pre_cash = sum(filter(None, [c.paid for c in certificates if c.shareholder.investor == i]))
#         pre_price = pre_cash / pre_shares if pre_shares else 0
#         pre_rata = pre_shares / total_pre_shares if pre_shares else 0
#         prorata_shares = investor_certs.prorata(new_money_shares)
#         prorata_cash = prorata_shares * price
#         converted_shares = investor_certs.exchanged(pre_valuation, price)
#         converted_cash = sum(filter(None, [c.outstanding_debt for c in certificates if c.shareholder.investor == i]))
#         converted_price = converted_cash / converted_shares if converted_shares else 0
#         post_shares = sum(filter(None, [pre_shares, prorata_shares, converted_shares]))
#         post_cash = sum(filter(None, [pre_cash, prorata_cash, converted_cash]))
#         post_price = post_cash / post_shares if post_shares else 0
#         post_rata = post_shares / total_post_shares

#         total_pre_rata += pre_rata
#         total_post_rata += post_rata

#         posts.append({
#             'name': i.name,
#             'pre_shares': pre_shares,
#             'pre_cash': pre_cash,
#             'pre_price': pre_price,
#             'pre_rata': pre_rata,
#             'prorata_shares': prorata_shares,
#             'prorata_cash': prorata_cash,
#             'converted_shares': converted_shares,
#             'converted_cash': converted_cash,
#             'converted_price': converted_price,
#             'post_shares': post_shares,
#             'post_cash': post_cash,
#             'post_price': post_price,
#             'post_rata': post_rata,
#         })

#     # Create and append the warrants list
#     warrants_pre_shares = certificates.warrants
#     warrants_pre_rata = warrants_pre_shares / total_pre_shares
#     warrants_post_shares = warrants_pre_shares
#     warrants_post_rata = warrants_pre_shares / total_post_shares

#     total_pre_rata += warrants_pre_rata
#     total_post_rata += warrants_post_rata

#     posts.append({
#         'name': 'Warrant Coverage',
#         'pre_shares': warrants_pre_shares,
#         'pre_rata': warrants_pre_rata,
#         'post_shares': warrants_post_shares,
#         'post_rata': warrants_post_rata

#     })
#     # Create and append the options granted list
#     granted_pre_shares = certificates.outstanding_options
#     granted_pre_rata = granted_pre_shares / total_pre_shares
#     granted_post_shares = granted_pre_shares
#     granted_post_rata = granted_pre_shares / total_post_shares

#     total_pre_rata += granted_pre_rata
#     total_post_rata += granted_post_rata

#     posts.append({
#         'name': 'Options Outstanding',
#         'pre_shares': granted_pre_shares,
#         'pre_rata': granted_pre_rata,
#         'post_shares': granted_post_shares,
#         'post_rata': granted_post_rata

#     })

#     # Create and append the available option list
#     available_pre_shares = certificates.available
#     available_pre_rata = available_pre_shares / total_pre_shares
#     available_post_shares = available_pre_shares + new_pool_shares
#     available_post_rata = available_post_shares / total_post_shares

#     total_pre_rata += available_pre_rata
#     total_post_rata += available_post_rata

#     posts.append({
#         'name': 'Options Available',
#         'pre_shares': available_pre_shares,
#         'pre_rata': available_pre_rata,
#         'post_shares': available_post_shares,
#         'post_rata': available_post_rata
#     })

#     # Finally, append the totals
#     posts.append({
#         'name': "Total",
#         'pre_shares': total_pre_shares,
#         'pre_cash': total_pre_cash,
#         'pre_rata': total_pre_rata,
#         'prorata_shares': new_prorata_shares,
#         'prorata_cash': total_prorata_cash,
#         'converted_shares': new_converted_shares,
#         'converted_cash': total_converted_cash,
#         'post_shares': total_post_shares,
#         'post_cash': total_post_cash,
#         'post_rata': total_post_rata
#     })

#     table = FinancingTable(posts)
#     RequestConfig(request, paginate={"per_page": 100}).configure(table)

#     proforma = {
#         'price': price,
#         'new_options': (available_post_shares - available_pre_shares),
#         'new_shares': new_investor_shares}
#     return render(request, 'financing.html', {'table': table, 'proforma': proforma})


def financing(request, new_money, pre_valuation, pool_rata):
    """Renders the financing table"""

    new_money = float(new_money)
    pre_valuation = float(pre_valuation)
    pool_rata = float(pool_rata)/100

    # get the objects needed for the page
    certificates = Certificate.objects.select_related()

    # get the proforma
    proforma = proforma2(new_money, pre_valuation, pool_rata)

    # populate the variables
    price = proforma['price']
    new_investor_shares = proforma['new_investor_shares']
    new_pool_shares = proforma['new_pool_shares']
    new_money_shares = proforma['new_money_shares']
    new_prorata_shares = proforma['new_prorata_shares']
    new_converted_shares = proforma['new_converted_shares']
    available = proforma['available']

    # set the 'globals'
    total_pre_shares = available + certificates.converted

    total_pre_cash = certificates.paid

    total_prorata_cash = new_prorata_shares * price
    total_converted_cash = certificates.outstanding_debt

    total_post_shares = sum([
        total_pre_shares,
        new_money_shares,
        new_converted_shares,
        new_pool_shares])

    total_post_cash = sum(filter(
        None, [total_pre_cash, new_money, total_converted_cash]))

    # Instantiate the context
    posts = []

    # Create the New Investor row
    new_investor_cash = new_money - total_prorata_cash
    new_investor_rata = new_investor_shares / total_post_shares

    total_pre_rata = 0
    total_post_rata = new_investor_rata

    posts.append({
        'security': 'New Issue',
        'name': 'New Investor',
        'pre_shares': '',
        'pre_cash': '',
        'pre_price': '',
        'pre_rata': '',
        'prorata_shares': '',
        'prorata_cash': '',
        'converted_shares': '',
        'converted_cash': '',
        'converted_price': '',
        'post_shares': new_investor_shares,
        'post_cash': new_investor_cash,
        'post_price': price,
        'post_rata': new_investor_rata

    })

    # Create the investor list
    investor_certificates = certificates.filter(
        security__security_type__in=[
            SECURITY_TYPE_COMMON,
            SECURITY_TYPE_CONVERTIBLE,
            SECURITY_TYPE_PREFERRED]).order_by('security__security_type', 'shareholder')

    for c in investor_certificates:
        pre_shares = c.outstanding_shares
        pre_cash = c.paid
        pre_price = c.discounted_price
        pre_rata = pre_shares / total_pre_shares
        prorata_shares = c.prorata(new_money_shares)
        prorata_cash = prorata_shares * price
        converted_shares = c.exchanged(pre_valuation, price)
        converted_cash = c.outstanding_debt
        converted_price = c.discounted_price
        post_shares = sum(filter(None, [pre_shares, prorata_shares, converted_shares]))
        post_cash = sum(filter(None, [pre_cash, prorata_cash, converted_cash]))
        post_price = 0 #post_cash / post_shares if post_shares else 0
        post_rata = post_shares / total_post_shares

        total_pre_rata += pre_rata
        total_post_rata += post_rata
        if not pre_shares and not converted_shares:
            continue
        posts.append({
            'security': c.security,
            'name': c.shareholder.investor,
            'pre_shares': pre_shares,
            'pre_cash': pre_cash,
            'pre_price': pre_price,
            'pre_rata': pre_rata,
            'prorata_shares': prorata_shares,
            'prorata_cash': prorata_cash,
            'converted_shares': converted_shares,
            'converted_cash': converted_cash,
            'converted_price': converted_price,
            'post_shares': post_shares,
            'post_cash': post_cash,
            'post_price': post_price,
            'post_rata': post_rata,
        })

    # Create and append the warrants list
    warrants_pre_shares = certificates.warrants
    warrants_pre_rata = warrants_pre_shares / total_pre_shares
    warrants_post_shares = warrants_pre_shares
    warrants_post_rata = warrants_pre_shares / total_post_shares

    total_pre_rata += warrants_pre_rata
    total_post_rata += warrants_post_rata

    posts.append({
        'name': 'Warrant Coverage',
        'pre_shares': warrants_pre_shares,
        'pre_rata': warrants_pre_rata,
        'post_shares': warrants_post_shares,
        'post_rata': warrants_post_rata

    })
    # Create and append the options granted list
    granted_pre_shares = certificates.outstanding_options
    granted_pre_rata = granted_pre_shares / total_pre_shares
    granted_post_shares = granted_pre_shares
    granted_post_rata = granted_pre_shares / total_post_shares

    total_pre_rata += granted_pre_rata
    total_post_rata += granted_post_rata

    posts.append({
        'name': 'Options Outstanding',
        'pre_shares': granted_pre_shares,
        'pre_rata': granted_pre_rata,
        'post_shares': granted_post_shares,
        'post_rata': granted_post_rata

    })

    # Create and append the available option list
    available_pre_shares = certificates.available
    available_pre_rata = available_pre_shares / total_pre_shares
    available_post_shares = available_pre_shares + new_pool_shares
    available_post_rata = available_post_shares / total_post_shares

    total_pre_rata += available_pre_rata
    total_post_rata += available_post_rata

    posts.append({
        'name': 'Options Available',
        'pre_shares': available_pre_shares,
        'pre_rata': available_pre_rata,
        'post_shares': available_post_shares,
        'post_rata': available_post_rata
    })

    # Finally, append the totals
    posts.append({
        'name': "Total",
        'pre_shares': total_pre_shares,
        'pre_cash': total_pre_cash,
        'pre_rata': total_pre_rata,
        'prorata_shares': new_prorata_shares,
        'prorata_cash': total_prorata_cash,
        'converted_shares': new_converted_shares,
        'converted_cash': total_converted_cash,
        'post_shares': total_post_shares,
        'post_cash': total_post_cash,
        'post_rata': total_post_rata
    })

    table = FinancingTable(posts)
    RequestConfig(request, paginate={"per_page": 100}).configure(table)

    proforma = {
        'price': price,
        'new_options': (available_post_shares - available_pre_shares),
        'new_shares': new_investor_shares}
    return render(request, 'financing.html', {'table': table, 'proforma': proforma})




# @login_required
def liquidation(request, purchase_price):
    """Renders the liquidation analysis."""
    purchase_cash = float(purchase_price)
    round_price = share_price(purchase_cash)

    certificates = Certificate.objects.select_related().order_by('shareholder__investor')

    liquidation = []

    for certificate in certificates:
        if certificate.vested == 0:
            continue
        proceeds = certificate.liquidated * round_price[certificate.security.seniority]
        liquidation.append({
            'investor': certificate.shareholder.investor.name,
            'investor_slug': certificate.shareholder.investor.slug,
            'shareholder': certificate.shareholder.name,
            'shareholder_slug': certificate.shareholder.slug,
            'certificate': certificate.name,
            'certificate_slug': certificate.slug,
            'vested': certificate.vested,
            'liquidated': certificate.liquidated,
            'preference': certificate.preference,
            'proceeds': proceeds,
            'proceeds_rata': proceeds/purchase_cash
        })

    table = LiquidationTable(liquidation)
    RequestConfig(request, paginate={"per_page": 100}).configure(table)
    return render(
            request, 'liquidation.html', {'table': table})

