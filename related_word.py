# -*- coding: utf8 -*-

import csv
import json
import urllib2
from xml.dom import minidom
from contextlib import closing

BASE_URL_JSON  = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
BASE_URL       = 'http://suggestqueries.google.com/complete/search?client=toolbar&q='

def build_search_url(request_query, json=False):
    """Build up search url that is passed to defined url"""
    if request_query is None:
        raise ValueException('No request_query')

    query = urllib2.quote('"' + request_query.encode('utf-8') + '"')
    if json:
        return BASE_URL_JSON + query
    return BASE_URL + query

def fetch_search_url(url):
    if url is None:
        raise ValueException('No url')

    with closing(urllib2.urlopen(url.encode('utf-8'))) as response:
        return response.read()

def parse_search_result(search_result_list, json=False):
    """Try to parse JSON/XML data as python data structure

    Basically, this function will return the array structure of
    what search engine returned.
    """
    if search_result_list is None or len(search_result_list) is 0:
        raise ValueException('No search_result')

    if json:
        return json.loads(search_result_list)[1]

    search_result = minidom.parseString(search_result_list).getElementsByTagName('suggestion')
    return set([result.attributes['data'].value for result in search_result])

def search_relative(input_list, result_dict = {}):
    """Actual search function to organize all of functions above(main function?)

    dispatch the search urls as much as input_list has
    make an output list/set which mapped to input_list keywords
    """
    if input_list is None:
        raise ValueException('No input_list')

    if len(input_list) is 0 \
            or _check_dict_depth(result_dict):
        return result_dict

    for word in input_list:
        if _check_combo_length(word):
            continue
        fetch_result = parse_search_result(fetch_search_url(build_search_url(word)))
        if word in fetch_result:
            fetch_result.remove(word)
        if word not in result_dict:
            result_dict[word] = fetch_result
        else:
            result_dict[word] = set(result_dict[word]).union(fetch_result)
        search_relative(fetch_result, result_dict)
    return result_dict

def _check_combo_length(query_word, max_combo=3):
    if query_word is None:
        raise ValueException('No query')
    return len(query_word.split()) > max_combo

def _check_word_combo_length(query_set, max_combo=3):
    if query_set is None:
        raise ValueException('No query')

    for item in query_set:
        if len(item.split()) > max_combo:
            return True
    return False

def _check_dict_depth(word_dict, max_deep=3):
    """Checks if any of dict entries reaches max_deep
    Default deepness is 3
    Since the result word is either a single word or a combination of
    keywords. So an element of one list will be consist of such result,
    and a list of certain keyword will have multi-dimentional list
    """
    if word_dict is None:
        raise ValueException('No word_dict')

    result = False
    for values in word_dict.values():
        result = _check_word_combo_length(values)
    return result

def read_csv(file_path):
    if file_path is None:
        raise ValueException('No file_path')

    input_list = []
    with open(file_path, 'r') as csv_file:
        for input_line in csv.reader(csv_file):
           input_list.extend(input_line)

    return input_list

def output_format(search_data):
    """build up string object with comma splited, multi-linebroken string"""
    if search_data is None:
        raise ValueException('No search_data')

    _output = ''
    return False

def write_csv(file_path, search_data):
    """Open the file descripter
    write out all search data, the search data will be in either list or dict
    Close the file descripter
    """
    if file_path is None:
        raise ValueException('No file_path to write')

    with open(file_path, 'w') as csv_file:
        csv_file.write(output_format(search_data))

def main():
    """TODO List:
    Get the initial inputs from given CSV file in list structure
    Throw these inputs into google suggestion
    - Get these results in list form
    - recursively find words, use dict and set
    Gather the results in CSV format, and output(on stdout?)
    """
    pass

if __name__ == '__main__':
    main()
