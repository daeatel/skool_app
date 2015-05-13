from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^results/$', views.search, name='search'),
    url(r'^add_site/$', views.add_site, name='add_site'),
    url(r'^monitor/(?P<url>.+)/$', views.monitor, name='monitor')
)
