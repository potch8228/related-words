# -*- coding: utf8 -*-

import argparse
import csv
import json
import urllib2
from contextlib import closing
from xml.dom import minidom

BASE_URL_JSON = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
BASE_URL      = 'http://suggestqueries.google.com/complete/search?client=toolbar&q='

parser = argparse.ArgumentParser()
parser.add_argument('input_csv',  help='input word list in CSV file format')
parser.add_argument('output_csv', help='output CSV file')
parser.add_argument('-c', '--combination', \
        type=int, default=3, help='maximum word combinations to search')
parser.add_argument('-e', '--encoding', \
        type=str, default='utf-8', help='output file encoding')

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

    search_result = minidom.parseString(search_result_list) \
                            .getElementsByTagName('suggestion')
    return set([result.attributes['data'].value for result in search_result])

def search_relative(input_list, result_dict = {}, max_combo=3):
    """Actual search function to organize all of functions above(main function?)

    dispatch the search urls as much as input_list has
    make an output list/set which mapped to input_list keywords
    """
    if input_list is None:
        raise ValueException('No input_list')

    if len(input_list) is 0 \
            or _check_dict_depth(result_dict, max_combo):
        return result_dict

    for word in input_list:
        if _check_combo_length(word, max_combo):
            continue
        fetch_result = parse_search_result( \
                fetch_search_url( \
                    build_search_url(word) \
                ) \
            )
        if word in fetch_result:
            fetch_result.remove(word)
        if word not in result_dict:
            result_dict[word] = fetch_result
        else:
            result_dict[word] = set(result_dict[word]).union(fetch_result)
        search_relative(fetch_result, result_dict)
    return result_dict

def _check_combo_length(query_word, max_combo):
    if query_word is None:
        raise ValueException('No query')
    return len(query_word.split()) >= max_combo

def _check_word_combo_length(query_set, max_combo):
    if query_set is None:
        raise ValueException('No query')

    for item in query_set:
        if len(item.split()) >= max_combo:
            return True
    return False

def _check_dict_depth(word_dict, max_deep):
    """Checks if any of dict entries reaches max_deep
    Default deepness is 3
    Since the result word is either a single word or a combination of
    keywords. So an element of one list will be consist of such result,
    and a list of certain keyword will have multi-dimentional list
    """
    if word_dict is None:
        raise ValueException('No word_dict')

    result = False
    for value in word_dict.values():
        result = _check_word_combo_length(value, max_deep)
    return result

def read_csv(file_path, encoding='shift_jis'):
    if file_path is None:
        raise ValueException('No file_path')

    input_list = []
    with open(file_path, 'r') as csv_file:
        reader = UnicodeReader(csv_file, encoding=encoding)
        for input_data in reader:
            input_list.extend(input_data)

    return input_list

def write_csv(file_path, search_data, encoding='shift_jis'):
    if file_path is None:
        raise ValueException('No file_path to write')

    with open(file_path, 'w') as csv_file:
        writer = UnicodeWriter(csv_file, encoding=encoding)
        for key in sorted(search_data):
            _output_list = list(search_data[key])
            _output_list.insert(0, key)
            writer.writerow(_output_list)

import codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
#        self.writer.writerow([s for s in row])
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def main():
    args = parser.parse_args()
    if args.input_csv is None \
        or args.output_csv is None:
        parser.print_usage()
        exit(1)

    write_csv(args.output_csv, \
            search_relative( \
                read_csv(args.input_csv, encoding=args.encoding)\
                , max_combo=args.combination \
            ) \
    )

if __name__ == '__main__':
    main()
