

def test_template(request_client):
    client = request_client()

    response = client.get('/sample_view_1/').content.decode()
    assert "'htmx:configRequest'" in response
    assert '<script src="https://unpkg.com/' in response
