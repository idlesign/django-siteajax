from datetime import datetime
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from siteajax.toolbox import Ajax, AjaxResponse, ajax_dispatch


def replacer1(request: HttpRequest):
    return HttpResponse(f'first replaced {datetime.now()}')


def replacer2(request: HttpRequest):
    return HttpResponse(f'second replaced {datetime.now()}')


def get_uid(request: HttpRequest):
    return HttpResponse(uuid4())


@ajax_dispatch({
    'replacer-1': replacer1,
    'replacer-2': replacer2,
    'some_uuid': get_uid,
})
def index(request: HttpRequest):
    return render(request, 'index.html')


def sample_1(request: HttpRequest):

    ajax: Ajax = request.ajax

    if ajax:
        response = HttpResponse(f'{datetime.now()}')

        response = AjaxResponse(response)
        response.trigger_event(name='fireThis', kwargs={'one': {'two': 3}})

        return response

    return HttpResponse('not ajax')
