Django ESV
==========

A some snippets for working with the `ESV Bible API`_

Some a `Django Inlines`_ style inline and a template tag.

Right now all they do is return the (x)html snippet provided by the ESV API and
provide clean ways to tweak the options.

**Template tag**::

  {% load esv %}
  {% passage reference [headings on] [audio off] [footnotes on] %}

Where reference is a string that the ESV can use as a query, or an context 
var that resolves to such a string.

Examples::

  {% passage "Genesis 1:1" %}
  {% passage "rom 3" %}
  {% passage "1 tim 3-4" footnotes on %}

**Inline**::

  {{ passage reference [headings=on] [audio=off] [footnotes=on] }}
  
Examples::

  {{ passage John 1 }}
  {{ passage John 2:1-3:18 footnotes=on }}
  {{ passage jhn 2 matt 3 }}

**Configuration**

django_esv has a single optional setting. Which controls where and how 
httplib2 stores it's http cache. It defaults to::

  ESV_HTTP_CACHE = '/tmp/esv_http_cache'


WARNING!
--------

The ESV client doesn't yet do any caching besides standard HTTP caching. 
You'll want to do output caching or wait for a real cache solution in django_esv.


Dependencies
************

* Django
* httplib2
* The inlines depend on `Django Inlines`_
* The tests depend on `django-test-extentions`_


.. _ESV Bible API: http://www.esvapi.org
.. _Django Inlines: http://github.com/mintchaos/django_inlines/tree/master
.. _django-test-extentions: http://github.com/garethr/django-test-extensions
