"""
Definition of urls for pentabank.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.views.generic.base import RedirectView
import pentabank
from pentabank.pentasit import views, forms

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

# define a site prefix: SET this for the production environment
# pfx = "ru/"
# SET this one for the development environment
pfx = ""


urlpatterns = [
    # Examples:
    url(r'^$', pentabank.pentasit.views.home, name='home'),
    url(r'^contact$', pentabank.pentasit.views.contact, name='contact'),
    url(r'^about', pentabank.pentasit.views.about, name='about'),
    url(r'^definitions$', RedirectView.as_view(url='/'+pfx+'admin/'), name='definitions'),
    url(r'^situations', RedirectView.as_view(url='/'+pfx+'admin/pentasit/situation/'), name='situations'),
    url(r'^overview', pentabank.pentasit.views.SituationListView.as_view(), name='overview'),
    url(r'^situation/$', pentabank.pentasit.views.SituationDetailView.as_view(), name='situation'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'pentasit/login.html',
            'authentication_form': pentabank.pentasit.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
