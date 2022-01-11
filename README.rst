django-siteajax
===============
https://github.com/idlesign/django-siteajax

|release| |lic| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/django-siteajax.svg
    :target: https://pypi.python.org/pypi/django-siteajax

.. |lic| image:: https://img.shields.io/pypi/l/django-siteajax.svg
    :target: https://pypi.python.org/pypi/django-siteajax

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/django-siteajax/master.svg
    :target: https://coveralls.io/r/idlesign/django-siteajax


Description
-----------

*Reusable application for Django bridging client and server sides*

Streamline your server and client interaction using declarative techniques
in your HTML and helpful abstractions from ``siteajax`` in your Python code.

.. note:: The client side of ``siteajax`` is powered by ``htmx``
  (the successor of ``intercooler.js``) - https://htmx.org/

Usage
-----

Somewhere in your ``views.py``:

.. code-block:: python

    from django.shortcuts import redirect, render
    from siteajax.toolbox import ajax_dispatch


    def get_news(request):
        news = ...  # Here we fetch some news from DB.
        # We could access `request.ajax` object properties
        # or even drive client side with the help
        # of siteajax.toolbox.AjaxResponse but for this demo
        # simple rendering is enough.
        return render(request, 'sub_news.html', {'news': news})

    @ajax_dispatch({
        # Map request source element id (see html below)
        # to a handler.
        'news-list': get_news,
    })
    def index_page(request):
        """Suppose this view is served at /"""
        return render(request, 'index.html')


Now to your ``index.html``:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <!-- Get client library js from CDN. -->
        {% include "siteajax/cdn.html" %}
    </head>
    <body>
        <div id="news-list" hx-get hx-trigger="load"></div>
        <!-- The contents of the above div will be replaced
            with the news from your server automatically fetched on page load.
            Notice `hx-*` attributes driving htmx JS library.
            Also notice how `id="news-list"` is used by `@ajax_dispatch`
            view decorator (shown above). -->
    </body>
    </html>


At last ``sub_news.html`` (nothing special):

.. code-block:: html

    {% for item in news %}<div>{{ item.title }}</div>{% endfor %}


Documentation
-------------

https://django-siteajax.readthedocs.org/
