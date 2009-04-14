Django ESV
==========

A some snippets for working with the `ESV Bible API`_

Some inlines which depend on `Django Inlines`_ and template tags.

Right now all they do is return the (x)html snippet provided by the ESV API and
provide clean ways to tweak the options.


WARNING!
********

As of right now the esv client uses naive attribute caching to cut down on API
requests. It is not recommended for use in any production environments until
proper caching is in place.


Dependencies
************

* The inlines depend on `Django Inlines`_
* The tests depend on `django-test-extentions`_


.. _ESV Bible API: http://www.esvapi.org
.. _Django Inlines: http://github.com/mintchaos/django_inlines/tree/master
.. _django-test-extentions: http://github.com/garethr/django-test-extensions
