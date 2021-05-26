from siteajax.utils import Ajax


def test_event_header(request_get):
    request = request_get(**{
        'HTTP_Triggering-Event-URI-AutoEncoded': 'true',
        'HTTP_Triggering-Event': '%7B%0A%20%22isTrusted%22%3A%20true%2C%0A%20%22BUBBLING_PHASE%22%3A%203%0A%7D'
    })

    ajax = Ajax(request)
    event_data = ajax.event
    assert event_data == {'isTrusted': True, 'BUBBLING_PHASE': 3}

    # no data
    assert Ajax(request_get()).event == {}
