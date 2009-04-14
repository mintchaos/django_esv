from esv import esv, PassageNotFoundError, EsvQuotaExceededError
from django import template
from django.conf import settings


register = template.Library()


class PassageNode(template.Node):
    
    def __init__(self, reference, footnotes='off', audio='on', headings='off', **kwargs):
        on_off_map = { 'on': True, 'off': False }
        self.reference = template.Variable(reference)
        self.footnotes = on_off_map[footnotes]
        self.audio = on_off_map[audio]
        self.headings = on_off_map[headings]
        
    def render(self, context):
        passage = ""
        try:
            passage = esv.get_passage(self.reference.resolve(context), footnotes=self.footnotes, headings=self.headings, audio=self.audio)
        except (PassageNotFoundError, EsvQuotaExceededError):
            if settings.TEMPLATE_DEBUG:
                raise
        return passage


@register.tag
def passage(parser, token):
    """
    Looks up the specified reference and returns passage from ESV's bible API
    
    Syntax::
    
      {% passage reference [headings on] [audio off] [footnotes on] %}

    Where reference is a string that the ESV can use as a query, or an context 
    var that resolves to such a string.

    Examples::

      {% passage "Genesis 1:1" %}
      {% passage "rom 3" %}
      {% passage "1 tim 3-4" footnotes on %}
    
    """
    ALLOWED_ARGS = ['headings', 'footnotes', 'audio']
    ALLOWED_VALUES = ['on', 'off']
    
    args = token.split_contents()
    
    if not len(args) in (2, 4, 6, 8):
        raise template.TemplateSyntaxError("%r tag requires either 1, 3, 5 or 7 arguments." % args[0])
    
    reference = args[1]
    kwargs = {}
    if len(args) > 2:
        tuples = zip(*[args[2:][i::2] for i in range(2)])
        for k,v in tuples:
            if not k in ALLOWED_ARGS:
                raise template.TemplateSyntaxError("%r tag options arguments must be one of %s." % (args[0], ', '.join(ALLOWED_ARGS)))
            if not v in ALLOWED_VALUES:
                raise template.TemplateSyntaxError("the values for %r's arguments must be one of %s." % (args[0], ', '.join(ALLOWED_VALUES)))
            kwargs[str(k)] = str(v)

    return PassageNode(reference, **kwargs)
