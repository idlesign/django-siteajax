django-siteajax
===============
https://github.com/idlesign/django-siteajax

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/django-siteajax.svg
    :target: https://pypi.python.org/pypi/django-siteajax

.. |lic| image:: https://img.shields.io/pypi/l/django-siteajax.svg
    :target: https://pypi.python.org/pypi/django-siteajax

.. |ci| image:: https://img.shields.io/travis/idlesign/django-siteajax/master.svg
    :target: https://travis-ci.org/idlesign/django-siteajax

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/django-siteajax/master.svg
    :target: https://coveralls.io/r/idlesign/django-siteajax


Description
-----------

*Reusable application for Django bridging client and server sides with htmx*

Streamline you server and client interaction using declarative techniques
in your HTML and helpful abstractions from ``siteajax`` in your views.

.. note:: The client side of ``siteajax`` is powered by ``htmx``
  (the successor of ``intercooler.js``) - https://htmx.org/

Usage
-----

Somewhere in your ``views.py``:

.. code-block:: python

    from django.shortcuts import redirect, render
    from siteajax.toolbox import Ajax


    def index_page(request):
        """Suppose this view is served at /"""

        ajax: Ajax = request.ajax

        if ajax:
            news = ...  # Here we fetch some news from DB.
            # We can drive client side with the
            # help of siteajax.toolbox.AjaxResponse
            # but for this demo simple rendering is enough.
            return render(request, 'mytemplates/sub_news.html', {'news': news})

        return render(request, 'mytemplates/index.html')


Now to your ``mytemplates/index.html``:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <!-- Get client library js from CDN. -->
        {% include "siteajax/cdn.html" %}
    </head>
    <body>
        <div hx-get="/" hx-trigger="load"></div>
        <!-- The contents of the above div will be replaced
            with news from server automatically fetched on page load. -->
    </body>
    </html>


At last ``mytemplates/sub_news.html`` (nothing special):

.. code-block:: html

    {% for item in news %}<div>{{ item.title }}</div>{% endfor %}


Documentation
-------------

https://django-siteajax.readthedocs.org/
