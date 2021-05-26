from siteajax.utils import Source


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
