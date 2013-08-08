from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.captable.views',

    url(r'liquidation/$', 'liquidation_instructions', name='liquidation_instructions'),
    url(r'financing/$', 'financing_instructions', name='financing_instructions'),

    url(r'summary/$', 'summary', name='summary'),
    url(r'liquidation/(?P<purchase_price>\d+)$', 'liquidation_summary', name='liquidation_summary'),
    url(r'financing/(?P<new_money>\d+),(?P<pre_valuation>\d+),(?P<pool_rata>\d+)$', 'financing_summary', name='financing_summary'),

    url(r'security/$', 'security_list', name='security_list'),
    url(r'investor/$', 'investor_list', name='investor_list'),
    url(r'certificate/$', 'certificate_list', name='certificate_list'),

    url(r'security/(?P<security>[\w-]+)/$', 'security_detail', name='security_detail'),
    url(r'certificate/(?P<certificate>[\w-]+)/$', 'certificate_detail', name='certificate_detail'),
    url(r'investor/(?P<investor>[\w-]+)/$', 'investor_detail', name='investor_detail'),
)
