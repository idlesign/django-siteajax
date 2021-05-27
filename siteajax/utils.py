from json import dumps, loads
from typing import NamedTuple, Dict, Any
from urllib.parse import unquote

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirectBase


class Source(NamedTuple):
    """Describes an element sourcing (triggering) a request."""

    id: str
    """The id of the triggered element if exists."""

    name: str
    """The name of the triggered element if exists."""


class Ajax:
    """Describes additional data sent with Ajax request.

    .. note:: The object is lazily initialized to allow faster
        middleware processing.

        Without initialization you won't be able to access it's attributes.
        For initialization it's enough to check it in boolean context, e.g.::

            bool(Ajax(request))

            # or

            if request.ajax:
                ...

    """
    __slots__ = ['is_used', 'url', 'source', 'target', 'user_input', 'restore_history', '_request']

    def __init__(self, request: HttpRequest):
        self._request = request

    def _boot(self):
        headers = self._request.headers

        self.is_used: bool = headers.get('Hx-Request', '') == 'true'
        """Indicates whether Ajax request is issued."""

        self.restore_history: bool = headers.get('HX-History-Restore-Request', '') == 'true'
        """Indicates the client side request to get the entire page 
        (as opposed to a page fragment request), when the client was 
        unable to restore a browser history state from the cache.
        
        """

        self.url: str = headers.get('Hx-Current-Url', '')
        """The current URL of the browser."""

        self.source: Source = Source(
            id=headers.get('HX-Trigger', ''),
            name=headers.get('HX-Trigger-Name', ''),
        )
        """Describes an element sourcing (triggering) a request."""

        self.target: str = headers.get('HX-Target', '')
        """The id of the target element if it exists."""

        self.user_input: str = headers.get('HX-Prompt', '')
        """The user input to a prompt (hx-prompt)."""

    def __bool__(self):
        self._boot()
        return self.is_used

    @property
    def event(self) -> dict:
        """Returns a dictionary describing a triggering event.

        Requires `event-header` extension:
            https://htmx.org/extensions/event-header/

        """
        headers = self._request.headers

        data = headers.get('Triggering-Event', '')
        if not data:
            return {}

        # encoded = headers.get('Triggering-Event-Uri-Autoencoded', '') == 'true'
        data = unquote(data)

        return loads(data)


class AjaxResponse(HttpResponse):
    """Represents a response object capable of driving a client side."""

    __slots__ = [
        '_wrapped', '_headers', '_triggers',
        'js_redirect',
        'history_item', 'redirect', 'refresh',
    ]

    _trigger_stages = {
        'receive': 'HX-Trigger',
        'settle': 'HX-Trigger-After-Settle',
        'swap': 'HX-Trigger-After-Swap',
    }

    def __init__(self, response: HttpResponse, *, js_redirect: bool = True, **kwargs):
        """

        :param response: Base response object.

        :param js_redirect: Whether to convert a redirect response object
            into an instruction for a client js library.

            * True - redirect is handled by a client side js library. Js library
                will get a result from this response.

            * False - redirect is handled by a browser. Js library will get
                the result from an URL browser has redirected it to.

        """
        super().__init__(**kwargs)

        self._wrapped = response
        self.js_redirect: bool = js_redirect

        self._triggers: Dict[str, Dict[str, Any]] = {
            'receive': {},
            'settle': {},
            'swap': {},
        }

        self.history_item: str = ''
        """Allows to push a new url into the browser history stack."""

        self.redirect: str = ''
        """Instructs a client-side redirect to a new location."""

        self.refresh: bool = False
        """Instructs a client side to make full refresh of the page."""

    @property
    def wrapped_response(self) -> HttpResponse:
        """Returns an base response modified to allow client driving."""

        response = self._wrapped
        headers = getattr(response, 'headers', None)

        if headers is None:  # pragma: nocover
            # pre Django 3.2
            headers = response

        val = self.history_item
        if val:
            headers['HX-Push'] = val

        val = self.redirect
        if val:
            headers['HX-Redirect'] = val

        if self.redirect:
            headers['HX-Refresh'] = 'true'

        if self.js_redirect and isinstance(response, HttpResponseRedirectBase):
            self.redirect = response.url
            del headers['location']  # Do not trigger browser redirect

        # Now encode event triggers data.
        trigger_stages = self._trigger_stages

        for stage, events in self._triggers.items():

            if not events:
                continue

            header_key = trigger_stages.get(stage)

            if header_key:
                headers[header_key] = dumps(events, cls=DjangoJSONEncoder)

        return response

    def trigger_event(self, *, name: str, kwargs: Dict[str, Any] = None, step: str = 'receive'):
        """Can be used to trigger client side actions on the target element within a response.

        .. code-block::
            // Python
            response.trigger_event(name='myEvent', kwargs={'one': {'two': 3}})

            // JS
            document.body.addEventListener('myEvent', function(event){
                console.log(event.detail.one.two);
            })

        :param name: Event name to trigger.

        :param kwargs: Keyword arguments to pass to an event.
            Those will be available from event.detail object.

        :param step: When to trigger this event.

            https://htmx.org/docs/#request-operations

            * receive - trigger events as soon as the response is received. Default.
            * settle - trigger events after the settling step.
            * swap - trigger events after the swap step.

        """
        self._triggers[step][name] = kwargs or {}
