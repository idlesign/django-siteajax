from typing import Callable, Dict

from django.http import HttpResponse

from .utils import Ajax


def ajax_dispatch(views_map: Dict[str, Callable]) -> Callable:
    """Decorator. Allows ajax request dispatch based 
    on source html element identifiers.

    Useful in cases when various ajax calls have a single entry point view.

    .. code-block::
        // JS. Define an element with `id`.
        <button id="replaceit" hx-get="/">Push me</button>

        // Python. Define a handling view and an entry point view decorated.

        def do_replace(request):
            return HttpResponse('Thank you')

        @ajax_dispatch({
            'replaceit': do_replace,  # Map element id to a handler
            'prefixed-some-*': do_replace,  # Map several id with the same prefix
        })
        def index(request):
            return HttpResponse('not ajax')
     
    :param views_map: Map html elements IDs to handling functions.
        To match several IDs use start (*)

    """
    wildcards = {}
    ids = {}

    for key, handler in views_map.items():
        prefix, sep, _ = key.partition('*')

        if sep == '*':
            wildcards[prefix] = handler

        else:
            ids[key] = handler

    def ajax_view_(func: Callable) -> Callable:

        def view_wrapper(*fargs, **fkwargs) -> HttpResponse:

            request = fargs[0]

            if not hasattr(request, 'POST'):
                # Possibly a class-based view where 0-attr is `self`.
                request = fargs[1]

            if hasattr(request, 'ajax'):
                # Attribute is already set by middleware.
                ajax: Ajax = request.ajax

            else:
                # Initialize on fly.
                ajax = Ajax(request)
                request.ajax = ajax

            if ajax:
                source_id = ajax.source.id
                handling_view = ids.get(source_id)

                if not handling_view:
                    # Long way to process wildcards.
                    for id_prefix, handling in wildcards.items():
                        if source_id.startswith(id_prefix):
                            handling_view = handling
                            break

                if handling_view:
                    response = handling_view(*fargs, **fkwargs)
                    # Try to unwrap an AjaxResponse if any.
                    return getattr(response, 'wrapped_response', response)

            return func(*fargs, **fkwargs)

        return view_wrapper

    return ajax_view_
