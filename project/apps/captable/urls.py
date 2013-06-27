from django.conf.urls import patterns, url




urlpatterns = patterns(
    'apps.captable.views',




    url(r'^$', 'home', name='home'),

    url(r'company/(?P<company>[\w-]+)/$', 'company', name='company'),

    url(r'company/(?P<company>[\w-]+)/summary/$', 'summary', name='summary'),

    url(r'company/(?P<company>[\w-]+)/liquidation/(?P<purchase_price>\d+)$', 'liquidation', name='liquidation'),

    url(r'company/(?P<company>[\w-]+)/financing/(?P<new_money>\d+),(?P<pre_valuation>\d+),(?P<pool_rata>\d+)', 'financing', name='financing'),

    url(r'company/(?P<company>[\w-]+)/security/$', 'securities', name='securities'),
    url(r'company/(?P<company>[\w-]+)/investor/$', 'investors', name='investors'),
    url(r'company/(?P<company>[\w-]+)/shareholder/$', 'shareholders', name='shareholders'),
    url(r'company/(?P<company>[\w-]+)/certificate/$', 'certificates', name='certificates'),

    url(r'company/(?P<company>[\w-]+)/security/(?P<security>[\w-]+)/$', 'security', name='security'),
    url(r'company/(?P<company>[\w-]+)/certificate/(?P<certificate>[\w-]+)/$', 'certificate', name='certificate'),
    url(r'company/(?P<company>[\w-]+)/investor/(?P<investor>[\w-]+)/$', 'investor', name='investor'),
    url(r'company/(?P<company>[\w-]+)/shareholder/(?P<shareholder>[\w-]+)/$', 'shareholder', name='shareholder'),

)
