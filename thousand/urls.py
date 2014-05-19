from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'thoureport.views.smser', name='smser'),
    url(r'^sendsms$', 'thoureport.views.sender', name='sender'),
    url(r'^history$', 'thoureport.views.history', name='history'),
    # Examples:
    # url(r'^$', 'thousand.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
