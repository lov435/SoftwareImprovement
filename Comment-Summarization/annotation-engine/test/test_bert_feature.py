# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 01:31:07 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime
import unittest
from general.comment import Comment
from general.author import Author
from features.bert_feature import Bert_Feature

class testBertFeature(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.bertFeature = Bert_Feature()
        
    def testSimpleBert(self):
        a1 = Author("VHS", 5749570, 8192)
        c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17))
        self.assertEqual(self.bertFeature.cosine_similarity(c1, c1), 1.0)
        
    def testUnrelated(self):
        a1 = Author("SusanW", 5851520, 1461)
        c1 = Comment("@AmrishPandey &quot;finally block is not called in case of exception thrown by daemon thread&quot; - really?? [Citation Needed], I think? Actually <code>thread.stop()</code> does not necessarily prevent <code>finally</code> block from being executed.", a1, datetime.datetime(2017, 4, 25))
        a2 = Author("", 0, 0)
        c2 = Comment("@SusanW javarevisited.blogspot.in/2012/03/…", a2, datetime.datetime(2020, 6, 24)) #doesn't match any words in vocab
        similarity = self.bertFeature.cosine_similarity(c1, c2)
        print("Similarity on unrelated comments is " , similarity)
        self.assertNotEqual(similarity, 1.0)
        
    def testRelated(self):
        a1 = Author("SusanW", 5851520, 1461)
        c1 = Comment("Lambda is a good feature of Java 8", a1, datetime.datetime(2017, 4, 25))
        a2 = Author("", 0, 0)
        c2 = Comment("Java needed lambdas for a long time", a2, datetime.datetime(2020, 6, 24)) #doesn't match any words in vocab
        similarity = self.bertFeature.cosine_similarity(c1, c2)
        print("Similarity on related comments is ", similarity)
        self.assertNotEqual(similarity, 0.0)
        
if __name__ == '__main__':
    unittest.main()