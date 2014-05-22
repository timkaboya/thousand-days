from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'thoureport.views.smser', name='smser'),
    url(r'^sendsms$', 'thoureport.views.sender', name='sender'),

    url(r'^responses$', 'thoureport.views.responses', name='responses'),
    url(r'^modresp/(.+)$', 'thoureport.views.resp_mod', name='resp_mod'),

    url(r'^messages$', 'thoureport.views.messages', name='messages'),
    url(r'^reports$', 'thoureport.views.reports', name='reports'),
    # Examples:
    # url(r'^$', 'thousand.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
