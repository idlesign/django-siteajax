Quickstart
==========


Installation
~~~~~~~~~~~~

.. code-block::

    $ pip install django-siteajax


Configuration
~~~~~~~~~~~~~

In your project configuration file (usually ``settings.py``):

1. Add ``siteajax`` to ``INSTALLED_APPS``.
2. Add ``siteajax.middleware.ajax_handler`` to ``MIDDLEWARE``.


Usage
~~~~~

Somewhere in your ``views.py``:

.. code-block:: python

    from django.shortcuts import redirect, render
    from siteajax.toolbox import Ajax, AjaxResponse


    def index_page(request):
        """Suppose this view is served at /"""

        ajax: Ajax = request.ajax

        if ajax:

            news = ...  # Here we fetch some news from DB.

            response = render(request, 'mytemplates/sub_news.html', {'news': news})

            # Now we can already return the response as usual.
            # But let's instruct the client side
            # to do some tricks. For that we use AjaxResponse wrapper:
            response = AjaxResponse(response)
            # Let's trigger `newsReady` event defined on client side
            # and pass some params into it:
            response.trigger_event(name='newsReady', kwargs={'count': len(news)})

            return response

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

        <!-- Initialize CSRF token for Django (if you ever want to use POST/PUT etc.) -->
        <script>{% include "siteajax/init_csrf.js" %}</script>

        <script>
            document.body.addEventListener('newsReady', function(event){
               alert('News loaded: ' + event.detail.count);
            })
        </script>

    </body>
    </html>


At last ``mytemplates/sub_news.html`` (nothing special):

.. code-block:: html

    {% for item in news %}<div>{{ item.title }}</div>{% endfor %}


.. note:: See https://htmx.org/docs/ for more examples of client side

.. note:: See https://github.com/idlesign/django-siteajax/tree/master/demo for `siteajax` usage example.
