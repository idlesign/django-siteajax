from django.http import HttpResponse
from django.shortcuts import redirect, render

from siteajax.toolbox import Ajax, AjaxResponse


def sample_view_1(request):

    ajax: Ajax = request.ajax

    if ajax:
        do_redirect = request.GET.get('doredir') == '1'
        do_events = request.GET.get('doevents') == '1'

        if do_redirect:
            response = redirect('/somwhere/')

        else:
            response = HttpResponse('ajaxresp')

        response = AjaxResponse(response)

        response.history_item = '/otherurl/'
        response.redirect = '/here/'
        response.refresh = True

        if do_events:
            response.trigger_event(name='fireThis', kwargs={'one': {'two': 3}})
            response.trigger_event(name='fireThat')
            response.trigger_event(name='fireMe1', kwargs={'me': True}, step='swap')
            response.trigger_event(name='fireMe2', step='settle')

        return response

    return render(request, 'index.html')
