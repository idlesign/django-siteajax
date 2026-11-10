django-siteajax changelog
=========================


v1.0.0 [2023-01-21]
-------------------
! Dropped QA for Py 3.6. Added QA for Django 4.1.
+ CDN now points to htmx 1.8.5.


v0.5.0 [2021-05-28]
-------------------
+ Added wildcards IDs support for 'ajax_dispatch' decorator.
* Fixed 'AjaxResponse' handling by 'ajax_dispatch'.


v0.4.0 [2021-05-27]
-------------------
+ Middleware is now optional in certain cases.


v0.3.0 [2021-05-27]
-------------------
+ Ajax objects are now lazy to allow faster middleware processing.


v0.2.0 [2021-05-26]
-------------------
+ Added 'Ajax.restore_history' flag.
+ Added 'ajax_dispatch' decorator.
+ Added support for 'event-header' htmx extension ('Ajax.event').
+ JS. CDN is now linked to 1.4.0.


v0.1.0 [2021-05-25]
-------------------
+ Basic functionality.