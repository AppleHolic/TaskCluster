#!/Users/inosphe/anaconda/bin/python
# -*- coding: utf-8 -*-
import re
import os
from konlpy.tag import Mecab

def law_contents_to_file(content_list, file_path): #do all processes
    content_list = list(filter_html_text(content_list))
    content_list = list(split_line(content_list))
    content_list = list(analyzing_morphem(content_list))

    if os.path.exists(file_path):
        os.remove(file_path)
    mk_training_file(content_list, file_path)

def mk_training_file(content_list, file_path):
    with open(file_path, 'a') as a:
        for content in content_list:
            a.write(content)

def analyzing_morphem(content_list):
    mecab = Mecab()
    for idx, doc in enumerate(content_list):
        if idx % 5000 == 0 :
            print 'Morphem Analysis on %d' % idx
        yield ' '.join([part for part, pos in mecab.pos(doc.decode('utf-8'))]).encode('utf-8')

def split_line(content_list):
    for content in content_list:
        for item in content.split('.'):
            if len(item) > 3:
                yield item.strip()

def filter_html_text(content_list):
    #filtering with regular expression
    rep = get_special_html_char()
    matching = "(%s)" % '|'.join(rep)

    regex_html = re.compile(matching.decode('utf-8'))
    regex = re.compile(u'[^ㄱ-ㅣ가-힣 a-zA-Z\.]+')
    for content in content_list:
        content = regex_html.sub(' ', content) # substracts html ......
        content = regex.sub('', content).encode('utf-8') # substracts special characters...
        yield content

def get_special_html_char():
    return ['ndash', 'mdash', 'iexcl', 'iquest', 'quot', 'ldquo', 'rdquo', 'lsquo', 'rsquo', 'laqou', 'raqou', 'nbsp',
          'amp', 'cent', 'copy', 'divide', 'gt', 'lt', 'micro', 'middot', 'para', 'plusmn', 'euro', 'pound', 'reg', 'sect',
          'trade', 'yen', 'deg', 'aacute', 'agrave', 'acirc', 'aring', 'atilde', 'Atilde', 'auml', 'aellg', 'ccedil', 'eacute',
          'egrave', 'ecirc', 'euml', 'iacute', 'igrave', 'icirc', 'iuml', 'ntilde', 'oacute', 'ograve', 'ocirc', 'oslash', 'otilde'
          'ouml', 'szlig', 'uacute', 'ugrave', 'ucirc', 'uuml', 'yuml']
