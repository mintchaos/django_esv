import urllib
import httplib2
from django.conf import settings

class EsvClientError(Exception):
    pass

class PassageNotFoundError(EsvClientError):
    pass

class EsvQuotaExceededError(EsvClientError):
    pass


class EsvClient(object):
    def __init__(self, key='IP'):
        http_cache = getattr(settings, 'ESV_HTTP_CACHE', '/tmp/esv_http_cache')
        self.http = httplib2.Http(http_cache)
        self.key = key
        self._cache = {}
    
    def get_passage(self, passage, headings=False, audio=True, footnotes=False, audio_format="flash"):
        params_dict = {
            'passage': passage,
            'include-headings': headings,
            'include_footnotes': footnotes,
            'include-word-ids': False,
            'include-first-verse-numbers': False,
            'include-audio-link': audio,
            'audio-format': audio_format,
        }
        params = urllib.urlencode(params_dict).lower()
        # TODO: Check cache here
        resp, content = self.http.request("http://www.esvapi.org/v2/rest/passageQuery?key=%s&%s" % (self.key, params), "GET")
        if content.startswith("ERROR"):
            if content.lower().find('no results found') > 0:
                raise PassageNotFoundError
            if content.lower().find('you have exceeded your quota') > 0:
                raise EsvQuotaExceededError
            raise EsvClientError
        # TODO: Set cache here
        return content


# main instance of the esv client
esv = EsvClient()