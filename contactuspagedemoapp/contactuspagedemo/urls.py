from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',  # noqa

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        TemplateView.as_view(template_name="themes/homepage.html"),
        name='demoapp.homepage'),

    url(r'^contactus/', include('contactuspage.urls')),
)

urlpatterns += staticfiles_urlpatterns()
