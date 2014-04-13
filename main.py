# -*- coding: utf8 -*-

from xml.dom import minidom
import json

import httplib

SEARCH_URL       = 'http://suggestqueries.google.com/complete/search?client=firefox&'
SEARCH_URL_JSON  = 'http://suggestqueries.google.com/complete/search?output=toolbar&'
SEARCH_QUERY     = 'q='
# XML_RESULT_FIELD = ('CompleteSuggestion', 'suggestion', 'data')

def build_search_url(query=null, json=False):
    if json:
        return SEARCH_URL_JSON + SEARCH_QUERY + request_query
    else:
        return SEARCH_URL + SEARCH_QUERY + request_query

def fetch_search_url()

def parse_search_result(search_result_list=null, json=False):
    if search_result_list is None: # && len(search_result_list) is 0:
        return None

    if len(search_result_list) is 0:
        return None

    if json:
        return json.loads(search_result_list)[1]
    
#    return_list = []
    search_result = minidom.parseString(search_result_list).getElementsByTagName('suggestion')
#    search_result = search_result_dom.getElementsByTagName('suggestion');
#    for r in search_result
    return [result.attibutes['data'].value for result in search_result]


def main():
    echo 'hello!'

if __name__ == '__main__':
    main()
