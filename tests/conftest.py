import pytest
from django.http import HttpResponse
from pytest_djangoapp import configure_djangoapp_plugin
from pytest_djangoapp.fixtures.request import DjagoappClient

from siteajax.utils import Source


pytest_plugins = configure_djangoapp_plugin(
    extend_MIDDLEWARE=[
        'siteajax.middleware.ajax_handler',
    ],
)


class HtmxMock(DjagoappClient):

    @classmethod
    def get_extra(
        cls,
        source: Source = None,
        target: str = '',
        user_input: str = '',
        url: str = 'http://testhost/dummy/',
    ):
        extra = {
            'HTTP_HX-Request': 'true',
            'HTTP_HX-Current-Url': url,
        }

        if source:
            extra['HTTP_HX-Trigger'] = source.id
            extra['HTTP_HX-Trigger-Name'] = source.name

        if target:
            extra['HTTP_HX-Target'] = target

        if user_input:
            extra['HTTP_HX-Prompt'] = user_input

        return extra

    @classmethod
    def make_headers_a(cls, response: HttpResponse):

        headers = getattr(response, 'headers', getattr(response, '_headers', None))
        # _headers - in pre Django 3.2

        headers_a = {}

        for key, val in headers.items():
            if key.lower().startswith('hx'):
                if isinstance(val, tuple):  # pre 3.2
                    key, val = val[0], val[1]
                headers_a[key] = val

        response.headers_a = headers_a

    def get(
        self,
        path: str,
        data=None,
        source: Source = None,
        target: str = '',
        user_input: str = '',
        **kwargs
    ):
        extra = self.get_extra(
            source=source,
            target=target,
            user_input=user_input,
        )
        response = super().get(path, data=data, follow=False, secure=False, **extra, **kwargs)
        self.make_headers_a(response)

        return response


@pytest.fixture
def htmx():

    def request_client_(user=None, raise_exceptions=True, json=False, **kwargs) -> HtmxMock:
        return HtmxMock(
            user=user,
            raise_exceptions=raise_exceptions,
            json=json,
            **kwargs)

    return request_client_
