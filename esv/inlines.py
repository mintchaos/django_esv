from django_inlines.inlines import TemplateInline, InlineUnrenderableError
from esv import esv, PassageNotFoundError, EsvQuotaExceededError


class InlineQuotaExceededError(InlineUnrenderableError):
    pass

class InlinePassageNotFoundError(InlineUnrenderableError):
    pass


class PassageInline(TemplateInline):
    """
    An inline for retrieving passages from the ESV REST webservice.
    
    Takes any passage or passages and returns the ESV (x)html output for that 
    passage. ::
    
        {{ passage reference [arguments] }}
    
    Takes these arguments::
    
        headings=on/off default: off
        audio=on/off default: on
        footnotes=on/off default: off
    
    examples::
    
        {{ passage John 1 }}
        {{ passage John 2:1-3:18 footnotes=on }}
        {{ passage jhn 2 matt 3 }}
    
    """
    def __init__(self, value, footnotes='off', audio='on', headings='off', **kwargs):
        super(PassageInline, self).__init__(value, **kwargs)
        on_off_map = { 'on': True, 'off': False }
        self.footnotes = on_off_map[footnotes]
        self.audio = on_off_map[audio]
        self.headings = on_off_map[headings]
    
    def get_context(self):
        try:
            passage = esv.get_passage(self.value, footnotes=self.footnotes, headings=self.headings, audio=self.audio)
            return {'passage': passage }
        except PassageNotFoundError:
            raise InlinePassageNotFoundError
        except EsvQuotaExceededError:
            raise InlineQuotaExceededError
