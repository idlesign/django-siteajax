Advanced
========


Additional info from the client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``request.ajax`` object is ``siteajax.toolbox.Ajax``. It given you an access
to additional information received from the client:

* ``ajax.is_used`` - a flag indicating whether the request is Ajax or not
* ``ajax.restore_history`` - indicates the client side is requesting the entire page
  (as opposed to a page fragment request), when the client was unable to restore a browser history state
  from the cache.
* ``ajax.url`` - URL from the browser
* ``ajax.target`` - the id of the target element if it exists
* ``ajax.user_input`` - user input given to a prompt (hx-prompt)
* ``ajax.source`` - info about an element sourcing (triggered) the request (``id`` and ``name`` if any)


.. note:: The object is lazily initialized to allow faster
    middleware processing.

    Without initialization you won't be able to access it's attributes.

    For the initialization it's enough to check it in boolean context, e.g.::

        bool(Ajax(request))

        # or

        if request.ajax:
            ...



Driving the client
~~~~~~~~~~~~~~~~~~

Wrap your response into ``siteajax.toolbox.AjaxResponse`` to be able to instruct
your client to do thing:

.. code-block:: python

    from django.shortcuts import render
    from siteajax.toolbox import Ajax, AjaxResponse


    def index_page(request):

        response = render(request, 'some.html')

        # Wrap it
        response = AjaxResponse(response)

        # Let's trigger `fireThis` event after `swap` step
        response.trigger_event(name='fireThis', kwargs={'count': len(news)}, step='swap')

        # Add an item to browser history
        response.history_item = '/otherurl/'

        # Redirect with JS
        response.redirect = '/here/'

        # Refresh current page
        response.refresh = True

        return response


CSRF protection
~~~~~~~~~~~~~~~

Include ``siteajax/init_csrf.js`` in your template (page's ``body``) to initialize CSRF
token required to ``POST``, ``PUT``, ``DELETE``.

.. code-block:: html

    <script>{% include "siteajax/init_csrf.js" %}</script>


Include htmx from CDN
~~~~~~~~~~~~~~~~~~~~~

You can make use of including ``siteajax/cdn.html`` in your template (page's ``head``)
to get ``htmx`` right from a CDN.

.. code-block:: html

    {% include "siteajax/cdn.html" %}

.. note:: If you're not satisfied with the version included you can always
  define your own ``<script src=``.
