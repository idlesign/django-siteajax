from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from siteajax.toolbox import Ajax, AjaxResponse, ajax_dispatch


def sample_view_1(request: HttpRequest) -> HttpResponse:

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


def get_dispatched(request: HttpRequest) -> HttpResponse:
    return HttpResponse('dispatched')


@ajax_dispatch({
    'dispatchme': get_dispatched
})
def sample_view_2(request: HttpRequest) -> HttpResponse:
    return HttpResponse('notajax')


class SampleView3(View):

    def get_dispatched_2(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('dispatched')

    @ajax_dispatch({
        'dispatchme': get_dispatched_2
    })
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('notajax')
