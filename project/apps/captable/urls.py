from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.captable.views',

    url(r'summary/$', 'summary', name='summary'),
    url(r'liquidation/(?P<purchase_price>\d+)$', 'liquidation', name='liquidation'),
    url(r'financing/(?P<new_money>\d+),(?P<pre_valuation>\d+),(?P<pool_rata>\d+)', 'financing', name='financing'),

    url(r'security/$', 'security_list', name='security_list'),
    url(r'investor/$', 'investor_list', name='investor_list'),
    url(r'shareholder/$', 'shareholder_list', name='shareholder_list'),
    url(r'certificate/$', 'certificate_list', name='certificate_list'),

    url(r'security/(?P<security>[\w-]+)/$', 'security_detail', name='security_detail'),
    url(r'certificate/(?P<certificate>[\w-]+)/$', 'certificate_detail', name='certificate_detail'),
    url(r'investor/(?P<investor>[\w-]+)/$', 'investor_detail', name='investor_detail'),
    url(r'shareholder/(?P<shareholder>[\w-]+)/$', 'shareholder_detail', name='shareholder_detail'),
)
