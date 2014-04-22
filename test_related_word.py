# -*- encoding: utf8 -*-
import unittest
import related_word

class TestRelatedWord(unittest.TestCase):
#    def test_search_result(self):
#        raw_result_list = related_word.fetch_search_url(related_word.build_search_url(u'ロキソニン'))
#        result_list = related_word.parse_search_result(raw_result_list)
#        self.assertEqual(len(result_list), 10, 'Probably suggestions are less than 10')

    def test_search_relative(self):
#        sample_list = [u'ロキソニン', u'ボルタレン']
        sample_list = [u'test', u'sample']
        result_dict = related_word.search_relative(sample_list)
        self.assertNotEqual(len(result_dict), 0, 'Probably good structure')
        print result_dict

if __name__ == '__main__':
    unittest.main()
