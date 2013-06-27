from __future__ import division

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404)

from django.http import (
    HttpResponseServerError,
    HttpResponseForbidden)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig


from .tables import (
    # InvestorsTable,
    # ShareholdersTable,
    # SecuritiesTable,
    LiquidationTable,
    FinancingTable,
    CertificateTable,
    CommonTable,
    PreferredTable,
    ConvertibleTable,
    WarrantTable,
    OptionTable)

from .models import (
    Transaction,
    Shareholder,
    Company,
    Security,
    Investor,
    Certificate)

from .constants import *


def home(request):
    companies = Company.objects.filter(owner=request.user.id)
    # companies = Company.objects.all()
    return render(request, 'home.html', {'companies': companies})


@login_required
def summary(request, company):
    """Renders the summary cap table."""

    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        securities = Security.objects.filter(
            company=company).order_by(
                'security_type', 'date')
        for security in securities:
            security.diluted_rata = security.converted / company.diluted
        return render(
            request, 'summary.html', {'securities': securities, 'company': company})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def financing(request, company, new_money, pre_valuation, pool_rata):
    """Renders the financing table"""

    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        new_money = float(new_money)
        pre_valuation = float(pre_valuation)
        pool_rata = float(pool_rata)/100

        # get the objects needed for the page
        investors = Investor.objects.select_related().filter(
            shareholder__certificate__security__company=company).filter(
                shareholder__certificate__security__security_type__in=[
                    SECURITY_TYPE_COMMON,
                    SECURITY_TYPE_CONVERTIBLE,
                    SECURITY_TYPE_PREFERRED]).distinct()

        certificates = Certificate.objects.select_related().filter(
            security__company=company)

        # get the proforma
        proforma = company.proforma(new_money, pre_valuation, pool_rata)

        # populate the variables
        price = proforma['price']
        new_investor_shares = proforma['new_investor_shares']
        new_pool_shares = proforma['new_pool_shares']
        new_money_shares = proforma['new_money_shares']
        new_prorata_shares = proforma['new_prorata_shares']
        new_converted_shares = proforma['new_converted_shares']

        # set the 'globals'
        total_pre_shares = company.diluted
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
        for i in investors:
            investor_certs = certificates.filter(
                shareholder__investor=i)
            pre_shares = investor_certs.outstanding_shares
            if pre_shares == 0:
                continue
            pre_cash = sum(filter(None, [c.paid for c in certificates if c.shareholder.investor == i]))
            pre_price = pre_cash / pre_shares if pre_shares else 0
            pre_rata = pre_shares / total_pre_shares if pre_shares else 0
            prorata_shares = investor_certs.prorata(new_money_shares)
            prorata_cash = prorata_shares * price
            converted_shares = investor_certs.exchanged(pre_valuation, price)
            converted_cash = sum(filter(None, [c.outstanding_debt for c in certificates if c.shareholder.investor == i]))
            converted_price = converted_cash / converted_shares if converted_shares else 0
            post_shares = sum(filter(None, [pre_shares, prorata_shares, converted_shares]))
            post_cash = sum(filter(None, [pre_cash, prorata_cash, converted_cash]))
            post_price = post_cash / post_shares if post_shares else 0
            post_rata = post_shares / total_post_shares

            total_pre_rata += pre_rata
            total_post_rata += post_rata

            posts.append({
                'name': i.name,
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
        warrants_pre_shares = company.warrants
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
        granted_pre_shares = company.outstanding_options
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
        available_pre_shares = company.available
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
        return render(request, 'financing.html', {'table': table, 'proforma': proforma, 'company': company})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def liquidation(request, company, purchase_price):
    """Renders the liquidation analysis."""
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        purchase_cash = float(purchase_price)
        round_price = company.price(purchase_cash)

        investors = Investor.objects.select_related().filter(
            shareholder__certificate__security__company=company.id).distinct()

        certificates = Certificate.objects.select_related().filter(
            security__company=company)

        liquidation = []

        for investor in investors:
            vested = sum(filter(None, [c.vested for c in certificates if c.shareholder.investor == investor]))
            liquidated = sum(filter(None, [c.liquidated for c in certificates if c.shareholder.investor == investor]))
            proceeds = sum(filter(None, [(c.liquidated * round_price[c.security.seniority]) for c in certificates if c.shareholder.investor == investor]))
            preference = sum(filter(None, [c.preference for c in certificates if c.shareholder.investor == investor]))
            if liquidated == 0:
                continue
            liquidation.append({
                'name': investor.name,
                'company': company.slug,
                'investor_slug': investor.slug,
                'vested': vested,
                'liquidated': liquidated,
                'preference': preference,
                'proceeds': proceeds,
                'proceeds_rata': proceeds/purchase_cash
            })

        table = LiquidationTable(liquidation)
        RequestConfig(request, paginate={"per_page": 100}).configure(table)
        return render(
            request, 'liquidation.html', {'company': company, 'table': table})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def investors(request, company):
    """Renders the investor summary table"""
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        investors = get_list_or_404(Investor.objects.filter(
            shareholder__certificate__security__company=company).order_by(
                'name').distinct())
        return render(request, "investors.html", {'investors': investors, 'company': company})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def shareholders(request, company):
    """Renders the shareholder summary table"""
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        shareholders = get_list_or_404(Shareholder.objects.filter(
            certificate__security__company=company).order_by(
                'name').distinct())
        table = ShareholdersTable(shareholders)
        RequestConfig(request).configure(table)
        return render(request, "shareholders.html", {'table': table, 'shareholders': shareholders})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def securities(request, company):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        securities = get_list_or_404(Security.objects.order_by('security_type'), company=company)
        return render(request, "securities.html", {'securities': securities, 'company': company})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def certificates(request, company):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        certificates = get_list_or_404(Certificate.objects.filter(
            security__company=company))
        table = CertificateTable(certificates)
        RequestConfig(request).configure(table)
        return render(request, "certificates.html", {'table': table})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def company(request, company):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        company = get_object_or_404(Company, slug__iexact=company)
        return render(request, "company.html", {'company': company})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def security(request, company, security):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        security = get_object_or_404(Security, company__slug__iexact=company, slug__iexact=security)
        certificates = get_list_or_404(Certificate, security=security)
        if security.security_type == SECURITY_TYPE_COMMON:
            table = CommonTable(certificates)
        elif security.security_type == SECURITY_TYPE_PREFERRED:
            table = PreferredTable(certificates)
        elif security.security_type == SECURITY_TYPE_CONVERTIBLE:
            table = ConvertibleTable(certificates)
        elif security.security_type == SECURITY_TYPE_WARRANT:
            table = WarrantTable(certificates)
        elif security.security_type == SECURITY_TYPE_OPTION:
            table = OptionTable(certificates)
        else:
            raise HttpResponseServerError("No Securities")
        RequestConfig(request, paginate={"per_page": 100}).configure(table)
        return render(request, "security.html", {'security': security, 'table': table})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def investor(request, company, investor):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        investor = get_object_or_404(Investor, slug__iexact=investor)
        certificates = get_list_or_404(Certificate, shareholder__investor=investor)
        return render(request, "investor.html", {'investor': investor, 'certificates': certificates})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def shareholder(request, company, shareholder):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        shareholder = get_object_or_404(Shareholder, slug__iexact=shareholder)
        return render(request, "shareholder.html", {'shareholder': shareholder})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")


@login_required
def certificate(request, company, certificate):
    company = Company.objects.get(slug__iexact=company)
    if request.user in company.owner.all():
        certificate = get_object_or_404(Certificate, security__company__slug__iexact=company, slug__iexact=certificate)
        transactions = get_list_or_404(Transaction, certificate=certificate)
        return render(request, "certificate.html", {'certificate': certificate, 'transactions': transactions})
    else:
        return HttpResponseForbidden(
            "You do not have permission to view that item.")
