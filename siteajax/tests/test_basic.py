from django.http import HttpRequest, HttpResponse

from siteajax.decorators import ajax_dispatch
from siteajax.utils import Source, AjaxResponse


def test_headers(htmx):
    client = htmx()

    response = client.get(
        '/sample_view_1/',
        source=Source(id='myid', name='myname'),
        target='trgt',
        user_input='here i am',
        data={'doevents': 1}
    )

    assert response.status_code == 200
    assert response.headers_a == {
        'HX-Push': '/otherurl/',
        'HX-Redirect': '/here/',
        'HX-Refresh': 'true',
        'HX-Trigger': '{"fireThis": {"one": {"two": 3}}, "fireThat": {}}',
        'HX-Trigger-After-Settle': '{"fireMe2": {}}',
        'HX-Trigger-After-Swap': '{"fireMe1": {"me": true}}',
    }

    response = client.get(
        '/sample_view_1/',
        data={'doredir': 1}
    )
    assert response.status_code == 302
    assert response.headers_a == {'HX-Push': '/otherurl/', 'HX-Redirect': '/here/', 'HX-Refresh': 'true'}


def test_dispatch(htmx):
    client = htmx()

    def do_test(url: str):
        response = client.get(url, source=Source(id='dispatchme', name=''))
        assert response.content.decode() == 'dispatched'

        # not dispatched
        response = client.get(url, source=Source(id='unknown', name=''))
        assert response.content.decode() == 'notajax'

    # function based view
    do_test('/sample_view_2/')

    # class based view
    do_test('/sample_view_3/')


def test_decor_ajax_autoinit(request_get):

    def handler(request: HttpRequest):
        response = AjaxResponse(HttpResponse('fine'), js_redirect=True)
        response.history_item = 'addthis/'
        return response

    @ajax_dispatch({'me': handler})
    def my_view(request: HttpRequest):
        return HttpResponse('nope')

    request = request_get(**{
        'HTTP_HX-Request': 'true',
        'HTTP_HX-Trigger': 'me',
    })

    response = my_view(request)
    assert response.content == b'fine'
    assert response['HX-Push'] == 'addthis/'


def test_decor_wildcards(request_get):

    def handler(request: HttpRequest):
        return HttpResponse(request.ajax.source.id)

    @ajax_dispatch({
        'my-not': lambda request: HttpResponse('miss'),
        'my-id-*': handler,
    })
    def my_view(request: HttpRequest):
        return HttpResponse('nope')

    request = request_get(**{
        'HTTP_HX-Request': 'true',
        'HTTP_HX-Trigger': 'my-id-1234567',
    })

    response = my_view(request)
    assert response.content == b'my-id-1234567'
