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
        })
        def index(request):
            return HttpResponse('not ajax')
     
    :param views_map: Map html elements IDs to handling functions.

    """
    def ajax_view_(func: Callable) -> Callable:

        def view_wrapper(*fargs, **fkwargs) -> HttpResponse:

            ajax: Ajax = getattr(fargs[0], 'ajax', None)

            if ajax is None:
                # Possibly a class-based view where 0-attr is `self`.
                ajax = getattr(fargs[1], 'ajax', None)

            if ajax:
                handling_view = views_map.get(ajax.source.id)

                if handling_view:
                    return handling_view(*fargs, **fkwargs)

            response = func(*fargs, **fkwargs)

            return response

        return view_wrapper

    return ajax_view_
