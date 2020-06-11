# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 00:11:43 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime
import unittest
from general.comment import Comment
from general.author import Author
from features.time_features import Time_Features

class TestTimeFeatures(unittest.TestCase):
    def testTimeFeatures(self):
        print("Start the time feature test")
        a1 = Author("VHS", 5749570, 8192)
        a2 = Author("VHS", 5749570, 8192)
        c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17, 23, 8, 15))
        c2 = Comment("This is a bad answer", a2, datetime.datetime(2020, 5, 17, 23, 8, 55))
        
        timeFeatures = Time_Features()
        feature_dict = timeFeatures.getTimeFeature(c1, c2)
        self.assertEqual(feature_dict["tdiff_minute"], 1)
        
        c3 = Comment("This is an ok answer", a2, datetime.datetime(2020, 5, 21, 23, 8, 55))
        feature_dict = timeFeatures.getTimeFeature(c3, c2)
        self.assertEqual(feature_dict["tdiff_minute"], 0)
        self.assertEqual(feature_dict["tdiff_week"], 1)
        
        c4 = Comment("This is an ok answer", a2, datetime.datetime(2020, 2, 21, 23, 8, 55))
        feature_dict = timeFeatures.getTimeFeature(c4, c2)
        self.assertEqual(feature_dict["tdiff_minute"], 0)
        self.assertEqual(feature_dict["tdiff_week"], 0)
        self.assertEqual(feature_dict["tdiff_half_year"], 1)
        
        print("End of the time feature test")
        
    
if __name__ == '__main__':
    unittest.main()