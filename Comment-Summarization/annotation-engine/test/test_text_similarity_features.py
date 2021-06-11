# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 00:48:22 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime
import unittest
from general.comment import Comment
from general.author import Author
from features.text_similarity_features import Text_Similarity_Features

class TestTextSimilarityFeatures(unittest.TestCase):
    def testJaccardFeatures(self):
        print("Start the Jaccard feature test")
        a1 = Author("VHS", 5749570, 8192)
        a2 = Author("VHS", 5749570, 8192)
        c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17, 23, 8, 15))
        c2 = Comment("This is a bad answer", a2, datetime.datetime(2020, 5, 17, 23, 8, 55))
        
        textSimFeatures = Text_Similarity_Features()
        jaccard_score = textSimFeatures.jaccard_feature(c1, c2)
        
        self.assertEqual(jaccard_score, 2/3)


    def testJaccardFeatures(self):
        a1 = Author("VHS", 5749570, 8192)
        a2 = Author("VHS", 5749570, 8192)
        c1 = Comment("Worth noting PrintWriter", a1, datetime.datetime(2020, 5, 17, 23, 8, 15))
        c2 = Comment("PrintWriter is worth", a2, datetime.datetime(2020, 5, 17, 23, 8, 55))

        textSimFeatures = Text_Similarity_Features()
        jaccard_score = textSimFeatures.jaccard_code_feature(c1, c2)

        self.assertEqual(jaccard_score, 1.0)

if __name__ == '__main__':
    unittest.main()