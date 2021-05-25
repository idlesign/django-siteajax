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


def test_template(request_client):
    client = request_client()

    response = client.get('/sample_view_1/').content.decode()
    assert "'htmx:configRequest'" in response
