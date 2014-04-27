# -*- encoding: utf8 -*-
import unittest
import related_word
from os import path

class TestRelatedWord(unittest.TestCase):
    def setUp(self):
        self.sample_list_en = [u'test', u'sample']
        self.sample_list_ja = [u'ロキソニン', u'ボルタレン', u'バファリン']
        self.sample_dict    = { \
                                u'test' :set([u'a',u'b',u'c',u'd']), \
                                u'test2':set([u'e',u'f',u'g',u'h']) \
                                }
        self.sample_dict_ja = { \
                                u'テスト' :set([u'あ',u'い',u'う',u'え']), \
                                u'テスト2':set([u'か',u'き',u'く',u'け']) \
                                }
        self.single_search_word_en = u'test'
        self.single_search_word_ja = u'ロキソニン'

        self.test_input_csv  = 'test_result/test_input.csv'
        self.test_output_csv = 'test_result/test_output.csv'

        self.test_input_csv_ja  = 'test_result/test_input_ja.csv'
        self.test_output_csv_ja = 'test_result/test_output_ja.csv'

    def test_search_result(self):
        raw_result_list = related_word.fetch_search_url( \
                related_word.build_search_url(self.single_search_word_en) \
                )
        result_list     = related_word.parse_search_result(raw_result_list)
        self.assertEqual(len(result_list), 10,  \
                'Probably suggestions are less than 10')

    def test_search_relative_english(self):
        result_dict = related_word.search_relative(self.sample_list_en)
        self.assertNotEqual(len(result_dict), 0, 'Probably good structure')
#        print result_dict

    def test_search_relative_japanese(self):
        result_dict = related_word.search_relative(self.sample_list_ja)
        self.assertNotEqual(len(result_dict), 0, 'Probably good structure')
#        print result_dict

    def test_read_csv(self):
        result_list = related_word.read_csv(self.test_input_csv, encoding='utf-8')
        self.assertNotEqual(len(result_list), 0, 'Probably not reading...')
        self.assertTrue(self.single_search_word_en in result_list, \
                'Probably miss-conversion')

    def test_read_csv_japanese(self):
        result_list = related_word.read_csv(self.test_input_csv_ja, encoding='utf-8')
        self.assertNotEqual(len(result_list), 0, 'Probably not reading...')
        self.assertTrue(self.single_search_word_ja in result_list, \
                'Probably miss-conversion')

    def test_write_csv(self):
        related_word.write_csv(self.test_output_csv,self.sample_dict)
        self.assertTrue(path.exists(self.test_output_csv), 'No output file exist!')
        csv_content = related_word.read_csv(self.test_output_csv)
        len_dict = len(self.sample_dict)
        for v in self.sample_dict.values():
            len_dict += len(v)
        self.assertEqual(len(csv_content), len_dict, \
                'Input and Output has something wrong...' + str(len(csv_content)))

    def test_write_csv_japanese(self):
        related_word.write_csv(self.test_output_csv_ja,self.sample_dict_ja)
        self.assertTrue(path.exists(self.test_output_csv_ja), 'No output file exist!')
        csv_content = related_word.read_csv(self.test_output_csv_ja)
        len_dict = len(self.sample_dict_ja)
        for v in self.sample_dict.values():
            len_dict += len(v)
        self.assertEqual(len(csv_content), len_dict, \
                'Input and Output has something wrong...' + str(len(csv_content)))

if __name__ == '__main__':
    unittest.main()
