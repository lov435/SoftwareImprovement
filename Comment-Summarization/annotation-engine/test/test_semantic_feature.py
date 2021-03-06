# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:52:58 2020

@author: viral
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime
import unittest
from general.comment import Comment
from general.author import Author
from features.semantic_feature import Semantic_Feature

class testSemanticFeature(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.semFeature = Semantic_Feature()

    def testSimpleSemantics(self):
        a1 = Author("VHS", 5749570, 8192)
        c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17))
        self.assertEqual(self.semFeature.cosine_similarity(c1, c1), 1.0)

    def testUndefinedSemantics(self):
        a1 = Author("SusanW", 5851520, 1461)
        c1 = Comment("@AmrishPandey &quot;finally block is not called in case of exception thrown by daemon thread&quot; - really?? [Citation Needed], I think? Actually <code>thread.stop()</code> does not necessarily prevent <code>finally</code> block from being executed.", a1, datetime.datetime(2017, 4, 25))
        a2 = Author("", 0, 0)
        c2 = Comment("@SusanW javarevisited.blogspot.in/2012/03/…", a2, datetime.datetime(2020, 6, 24)) #doesn't match any words in vocab
        self.assertNotEqual(self.semFeature.cosine_similarity(c1, c2), 0.0)

    def testComparativeSemantics_Normal(self):
        a1 = Author("", 0, 0)
        c1 = Comment("I like junit", a1, datetime.datetime(2020, 1, 1))
        a2 = Author("", 0, 0)
        c2 = Comment("I like java", a2, datetime.datetime(2020, 1, 1))
        a3 = Author("", 0, 0)
        c3 = Comment("I like python", a3, datetime.datetime(2020, 1, 1))
        self.assertTrue(self.semFeature.cosine_similarity(c1, c2) > self.semFeature.cosine_similarity(c2, c3))
        self.assertTrue(self.semFeature.cosine_similarity(c1, c2) > self.semFeature.cosine_similarity(c1, c3))

    def testComparativeSemantics_Weighted(self):
        a1 = Author("", 0, 0)
        c1 = Comment("I like junit", a1, datetime.datetime(2020, 1, 1))
        a2 = Author("", 0, 0)
        c2 = Comment("I like java", a2, datetime.datetime(2020, 1, 1))
        a3 = Author("", 0, 0)
        c3 = Comment("I like python", a3, datetime.datetime(2020, 1, 1))
        self.assertTrue(self.semFeature.weighted_cosine_similarity(c1, c2) > self.semFeature.weighted_cosine_similarity(c2, c3))
        self.assertTrue(self.semFeature.weighted_cosine_similarity(c1, c2) > self.semFeature.weighted_cosine_similarity(c1, c3))

    def testWeightedIsDifferent(self):
        a1 = Author("", 0, 0)
        c1 = Comment("This is a good java answer", a1, datetime.datetime(2020, 1, 1))
        a2 = Author("", 0, 0)
        c2 = Comment("I like java", a2, datetime.datetime(2020, 1, 1))
        print(self.semFeature.weighted_cosine_similarity(c1, c2))
        print(self.semFeature.cosine_similarity(c1, c2))
        self.assertTrue(self.semFeature.weighted_cosine_similarity(c1, c2) != self.semFeature.cosine_similarity(c1, c2))

if __name__ == '__main__':
    unittest.main()