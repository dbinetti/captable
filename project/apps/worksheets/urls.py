from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.worksheets.views',

    url(r'summary/$', 'summary', name='summary'),
    url(r'liquidation/(?P<purchase_price>\d+)$', 'liquidation', name='liquidation'),
    url(r'financing/(?P<new_money>\d+),(?P<pre_valuation>\d+),(?P<pool_rata>\d+)', 'financing', name='financing'),
)
