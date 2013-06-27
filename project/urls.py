from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.captable.urls')),
)


# Uncomment these two lines and comment the stock url conf below
# if you wish to use the "Noncense" auth backend.

# urlpatterns += patterns(
#     url(r'^', include('noncense.urls')),)

urlpatterns += patterns(
    '',
    url(r'login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
