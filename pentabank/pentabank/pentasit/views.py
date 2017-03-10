"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.db.models.functions import Lower
from datetime import datetime
from pentabank.pentasit.models import *
from pentabank.settings import APP_PREFIX

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pentasit/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pentasit/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'pentasit/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


class SituationListView(ListView):
    """Show a list of situations"""

    model = Situation
    context_object_name='situation'
    template_name = 'pentasit/overview.html'
    order_cols = ['name', 'preposition', 'npType', 'penta','action']
    order_heads = [{'name': 'name', 'order': 'o=1', 'type': 'str'}, 
                   {'name': 'preposition', 'order': 'o=2', 'type': 'str'}, 
                   {'name': 'npType', 'order': 'o=3', 'type': 'str'}, 
                   {'name': 'penta', 'order': 'o=4', 'type': 'str'}, 
                   {'name': 'action', 'order': 'o=5', 'type': 'str'}]

    def get_context_data(self, **kwargs):
        # Get the base implementation first of the context
        context = super(SituationListView, self).get_context_data(**kwargs)
        # Add our own elements
        context['app_prefix'] = APP_PREFIX
        # Figure out which ordering to take
        order = 'name'
        initial = self.request.GET
        bAscending = True
        sType = 'str'
        if 'o' in initial:
            iOrderCol = int(initial['o'])
            bAscending = (iOrderCol>0)
            iOrderCol = abs(iOrderCol)
            order = self.order_cols[iOrderCol-1]
            sType = self.order_heads[iOrderCol-1]['type']
            if bAscending:
                self.order_heads[iOrderCol-1]['order'] = 'o=-{}'.format(iOrderCol)
            else:
                # order = "-" + order
                self.order_heads[iOrderCol-1]['order'] = 'o={}'.format(iOrderCol)
        if sType == 'str':
            qs = Situation.objects.order_by(Lower(order))
        else:
            qs = Situation.objects.order_by(order)
        if not bAscending:
            qs = qs.reverse()
        context['overview_list'] = qs.select_related()
        context['order_heads'] = self.order_heads
        # Return the calculated context
        return context



class SituationDetailView(DetailView):
    """Show details of a situation"""

    model = Situation
    context_object_name='situation'
