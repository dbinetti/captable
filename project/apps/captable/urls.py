from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.captable.views',

    url(r'summary/$', 'summary', name='summary'),
    url(r'liquidation/(?P<purchase_price>\d+)$', 'liquidation', name='liquidation'),
    url(r'financing/(?P<new_money>\d+),(?P<pre_valuation>\d+),(?P<pool_rata>\d+)', 'financing', name='financing'),

    url(r'security/$', 'securities', name='securities'),
    url(r'investor/$', 'investors', name='investors'),
    url(r'shareholder/$', 'shareholders', name='shareholders'),
    url(r'certificate/$', 'certificates', name='certificates'),

    url(r'security/(?P<security>[\w-]+)/$', 'security', name='security'),
    url(r'certificate/(?P<certificate>[\w-]+)/$', 'certificate', name='certificate'),
    url(r'investor/(?P<investor>[\w-]+)/$', 'investor', name='investor'),
    url(r'shareholder/(?P<shareholder>[\w-]+)/$', 'shareholder', name='shareholder'),
)
