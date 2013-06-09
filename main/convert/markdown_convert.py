# -*- coding: utf-8 -*-

import re

import markdown


# from base import BaseConvert


__all__ = ['MarkDownConvert', ]

# PRE_PATTERN = re.compile('<pre><code>.+?</code></pre>', re.DOTALL)
# CODE_PATTERN = re.compile('`{3}(.+?)\n(.+?)`{3}', re.DOTALL)

class MarkDownConvert(object):
    def convert(self, source):
        if not isinstance(source, unicode):
            source = source.decode('utf-8')
        md2html = markdown.markdown(source, safe_mode=False)

        md2html = re.sub("`{3,}[ \t]*(?P<brush>[a-zA-Z]+)",
                         '<pre class="brush: \g<brush>">' , md2html)
        md2html = re.sub("`{3,}\n", "</pre>\n",
                         md2html).replace("<pre><code>", "").replace("</code></pre>", "")

        return md2html
