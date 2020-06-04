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
from features.semantic_feature import Semantic_Feature

class testSemanticFeature(unittest.TestCase):

    def testSimpleSemantics(self):
        c1 = Comment("This is a good answer", "VHS", datetime.datetime(2020, 5, 17))
        semFeature = Semantic_Feature()
        self.assertEqual(semFeature.cosine_similarity(c1, c1), 1.0)


if __name__ == '__main__':
    unittest.main()