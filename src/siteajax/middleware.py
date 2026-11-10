from typing import Callable

from django.http import HttpRequest, HttpResponse

from .toolbox import Ajax


def ajax_handler(get_response: Callable) -> Callable:
    """This handles a request - response to making
    it easy to handle Ajax.

    :param get_response:

    """
    def handle(request: HttpRequest) -> HttpResponse:

        request.ajax = Ajax(request)

        response = get_response(request)

        # Try to unwrap an AjaxResponse if any.
        return getattr(response, 'wrapped_response', response)

    return handle
