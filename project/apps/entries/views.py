from __future__ import division

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from .tables import (
    ShareholderTable,
    CertificateTable,
    InvestorTable,
    SecurityTable,
)

from .models import (
    Shareholder,
    Security,
    Investor,
    Certificate)

from constants import *


@login_required
def investor_list(request):
    """Renders the investor table"""
    investors = get_list_or_404(Investor.objects.order_by('name'))
    table = InvestorTable(investors)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, "investor_list.html", {'table': table})


@login_required
def shareholder_list(request):
    """Renders the shareholder summary table"""
    shareholders = get_list_or_404(Shareholder.objects.order_by('name'))
    table = ShareholderTable(shareholders)
    RequestConfig(request).configure(table)
    return render(request, "shareholder_list.html", {'table': table})


@login_required
def security_list(request):
    securities = get_list_or_404(Security.objects.order_by('security_type'))
    table = SecurityTable(securities)
    RequestConfig(request).configure(table)
    return render(request, "security_list.html", {'table': table})


@login_required
def certificate_list(request):
    certificates = get_list_or_404(Certificate.objects.order_by('name'))
    table = CertificateTable(certificates)
    RequestConfig(request).configure(table)
    return render(request, "certificate_list.html", {'table': table})


@login_required
def security_detail(request, security):
    security = get_object_or_404(Security, slug__iexact=security)
    return render(request, "security_detail.html", {'security': security})


@login_required
def investor_detail(request, investor):
    investor = get_object_or_404(Investor, slug__iexact=investor)
    return render(request, "investor_detail.html", {'investor': investor})


@login_required
def shareholder_detail(request, shareholder):
    shareholder = get_object_or_404(Shareholder, slug__iexact=shareholder)
    return render(request, "shareholder_detail.html", {'shareholder': shareholder})


@login_required
def certificate_detail(request, certificate):
    certificate = get_object_or_404(Certificate, slug__iexact=certificate)
    return render(request, "certificate_detail.html", {'certificate': certificate})
