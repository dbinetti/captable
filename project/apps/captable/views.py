from __future__ import division

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django.db.models import (
    Sum,
)

from django_tables2 import RequestConfig

from .tables import (
    ShareholderTable,
    CertificateTable,
    InvestorTable,
    SecurityTable,
    LiquidationTable,
    FinancingTable,
)

from .models import (
    Shareholder,
    Security,
    Investor,
    Certificate)

from .managers import (
    share_price,
    proforma as proforma2
)

from .constants import *


# @login_required
def investor_list(request):
    """Renders the investor table"""
    investors = get_list_or_404(Investor.objects.order_by('name'))
    table = InvestorTable(investors)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, "investor_list.html", {'table': table})


# @login_required
def security_list(request):
    securities = get_list_or_404(Security.objects.order_by('security_type'))
    table = SecurityTable(securities)
    RequestConfig(request).configure(table)
    return render(request, "security_list.html", {'table': table})


# @login_required
def certificate_list(request):
    certificates = get_list_or_404(Certificate.objects.order_by('name'))
    table = CertificateTable(certificates)
    RequestConfig(request).configure(table)
    return render(request, "certificate_list.html", {'table': table})


# @login_required
def security_detail(request, security):
    security = get_object_or_404(Security, slug__iexact=security)
    return render(request, "security_detail.html", {'security': security})


# @login_required
def investor_detail(request, investor):
    investor = get_object_or_404(Investor, slug__iexact=investor)
    return render(request, "investor_detail.html", {'investor': investor})


# @login_required
def certificate_detail(request, certificate):
    certificate = get_object_or_404(Certificate, slug__iexact=certificate)
    return render(request, "certificate_detail.html", {'certificate': certificate})

def summary(request):
    """Renders the summary cap table."""
    securities = Security.objects.select_related().order_by('security_type', 'date')
    return render(
        request, 'summary.html', {'securities': securities})

def financing_instructions(request):
    return render(request, 'financing_instructions.html')


def liquidation_instructions(request):
    return render(request, 'liquidation_instructions.html')


def financing_summary(request, new_money, pre_valuation, pool_rata):
    """Renders the financing table"""

    # capture the parameters from the URL
    new_money = float(new_money)
    pre_valuation = float(pre_valuation)
    pool_rata = float(pool_rata)/100

    # calculate the proforma from those inputs
    proforma = proforma2(new_money, pre_valuation, pool_rata)

    # get all certificates
    certificates = Certificate.objects.select_related()

    # populate individual variables for ease of use
    price = proforma['price']
    new_investor_shares = proforma['new_investor_shares']
    new_investor_cash = proforma['new_investor_cash']
    new_pool_shares = proforma['new_pool_shares']
    new_money_shares = proforma['new_money_shares']
    new_prorata_shares = proforma['new_prorata_shares']
    new_prorata_cash = proforma['new_prorata_cash']
    new_converted_shares = proforma['new_converted_shares']
    available = proforma['available']

    pre_shares = certificates.outstanding + available
    pre_cash = certificates.paid
    new_shares = new_investor_shares + new_prorata_shares + new_converted_shares + new_pool_shares
    new_cash = new_investor_cash + new_prorata_cash
    post_shares = pre_shares + new_shares
    post_cash = pre_cash + new_cash

    # instantiate the context for the totals
    total = {
        'name': "Total",
        'price': price,
        'pre_shares': pre_shares,
        'pre_cash': pre_cash,
        'new_shares': new_shares,
        'new_cash': new_cash,
        'post_shares': post_shares,
        'post_cash': post_cash,
    }

    # get the objects needed for the detail
    certificates = Certificate.objects.select_related()
    securities = Security.objects.select_related()


    # Instantiate the context
    financing = []

    # Create the New Investor row
    new_investor_cash = new_money - new_prorata_cash
    new_investor_rata = new_investor_shares / total['post_shares']

    total_pre_rata = 0
    total_post_rata = new_investor_rata

    financing.append({
        'name': 'New Investor',
        'pre_shares': '',
        'pre_cash': '',
        'pre_rata': '',
        'new_shares': new_investor_shares,
        'new_cash': new_investor_cash,
        'post_shares': new_investor_shares,
        'post_cash': new_investor_cash,
        'post_rata': new_investor_rata,
    })

    # Get the current investor objects
    investors = Investor.objects.order_by('shareholder')

    for i in investors:
        name = i.name
        slug = i.slug
        pre_shares = i.outstanding
        pre_cash = i.paid
        pre_rata = pre_shares / total['pre_shares']

        prorata_shares = i.prorata(new_money_shares)
        prorata_cash = prorata_shares * price
        converted_shares = i.exchanged(pre_valuation, price)
        converted_cash = i.principal

        new_shares = prorata_shares + converted_shares
        new_cash = prorata_cash

        post_shares = pre_shares + new_shares
        post_cash = pre_cash + new_cash
        post_rata = post_shares / total['post_shares']

        total_pre_rata += pre_rata
        total_post_rata += post_rata

        # skip non-participating investors
        # if not pre_shares and not new_shares:
        #     continue
        financing.append({
            'name': name,
            'slug': slug,
            'pre_shares': pre_shares,
            'pre_cash': pre_cash,
            'pre_rata': pre_rata,
            'new_shares': new_shares,
            'new_cash': new_cash,
            'post_shares': post_shares,
            'post_cash': post_cash,
            'post_rata': post_rata,
        })

    # Create and append the available option list
    available_pre_shares = securities.filter(
        security_type=SECURITY_TYPE_OPTION).available
    available_pre_rata = available_pre_shares / total['pre_shares']
    available_post_shares = available_pre_shares + new_pool_shares
    available_post_rata = available_post_shares / total['post_shares']

    total_pre_rata += available_pre_rata
    total_post_rata += available_post_rata

    financing.append({
        'name': 'Options Available',
        'pre_shares': available_pre_shares,
        'pre_rata': available_pre_rata,
        'new_shares': available_post_shares - available_pre_shares,
        'new_cash': 0,
        'post_shares': available_post_shares,
        'post_rata': available_post_rata
    })

    return render(request, 'financing_summary.html', {'financing': financing, 'total': total})


# @login_required
def liquidation_summary(request, purchase_price):
    """Renders the liquidation analysis."""
    purchase_cash = float(purchase_price)
    # round_price = share_price(purchase_cash)
    # order_by = request.GET.get('order_by', 'shareholder__investor')

    investors = Investor.objects.select_related().order_by('name')
    certificates = Certificate.objects.select_related()

    total = {
        'proceeds': certificates.proceeds(purchase_cash),
        'preference': certificates.preference,
        'liquidated': certificates.liquidated,
    }

    liquidation = []
    for investor in investors:
        liquidation.append({
            'name': investor.name,
            'slug': investor.slug,
            'preference': investor.preference,
            'liquidated': investor.liquidated,
            'proceeds': investor.proceeds(purchase_cash),
            'proceeds_rata': investor.proceeds(purchase_cash) / total['proceeds']
        })

    return render(
            request, 'liquidation_summary.html', {'liquidation': liquidation, 'total': total})
