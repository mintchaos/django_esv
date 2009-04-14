# this bit is required to test templates without setting up a full django project.
from os.path import dirname, join, abspath
from django.conf import settings
template_dir = join(dirname(abspath(__file__)), 'templates')
print template_dir
settings.configure(
    TEMPLATE_DIRS=(template_dir,),
    TEMPLATE_LOADERS=('django.template.loaders.filesystem.load_template_source',),
    )


from esv import esv
from esv.inlines import PassageInline
import unittest
from django_inlines.inlines import Registry


class GetPassageTestCase(unittest.TestCase):
    
    def test_get_passage(self):
        value = esv.get_passage('gen 1:1')
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)
        cached = esv.get_passage('gen 1:1')
        self.assertEqual(cached, OUT)

    def test_get_passage_headings(self):
        value = esv.get_passage('gen 1:1', headings=True)
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><h3 id="p01001001.01-1">The Creation of the World</h3>\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)

    def test_get_passage_audio(self):
        value = esv.get_passage('gen 1:1', audio=False)
        OUT = '<div class="esv"><h2>Genesis 1:1</h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)

    def test_get_passage_footnotes(self):
        value = esv.get_passage('gen 1:7', footnotes=True)
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made<span class="footnote">&nbsp;<a href="#f1" id="b1" title="Or \'fashioned\'; also verse 16">[1]</a></span> the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n<div class="footnotes">\n<h3>Footnotes</h3>\n<p><span class="footnote"><a href="#b1" id="f1">[1]</a></span> <span class="footnote-ref">1:7</span> Or <em>fashioned</em>; also verse 16\n</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)
        value = esv.get_passage('gen 1:7', footnotes=False)
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)


class PassageInlineTestCase(unittest.TestCase):

    def setUp(self):
        settings.INLINE_DEBUG = True
        registry = Registry()
        registry.register('passage', PassageInline)
        self.inlines = registry
        
    def test_inline_passage(self):
        value = '{{ passage gen 1:1 }}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_headings(self):
        value = '{{ passage gen 1:1 headings=on }}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><h3 id="p01001001.01-1">The Creation of the World</h3>\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_audio(self):
        value = '{{ passage gen 1:1 audio=off }}'
        OUT = '<div class="esv"><h2>Genesis 1:1</h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_footnotes(self):
        value = '{{ passage gen 1:7 footnotes=on }}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made<span class="footnote">&nbsp;<a href="#f1" id="b1" title="Or \'fashioned\'; also verse 16">[1]</a></span> the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n<div class="footnotes">\n<h3>Footnotes</h3>\n<p><span class="footnote"><a href="#b1" id="f1">[1]</a></span> <span class="footnote-ref">1:7</span> Or <em>fashioned</em>; also verse 16\n</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)
        value = '{{ passage gen 1:7 footnotes=off }}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)


if __name__ == '__main__':
    unittest.main()