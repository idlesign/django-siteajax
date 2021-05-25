from datetime import datetime
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from siteajax.toolbox import Ajax, AjaxResponse


def index(request: HttpRequest):
    return render(request, 'index.html')


def sample_1(request: HttpRequest):

    ajax: Ajax = request.ajax

    if ajax:

        if ajax.source.id == 'some_uuid':
            return HttpResponse(uuid4())

        response = HttpResponse(f'{datetime.now()}')

        response = AjaxResponse(response)
        response.trigger_event(name='fireThis', kwargs={'one': {'two': 3}})

        return response

    return HttpResponse('not ajax')
