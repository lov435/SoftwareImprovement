# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:52:58 2020

@author: viral
"""

import datetime
from general.comment import Comment
from features.speaker_feature import Speaker_Feature

def testSameSpeaker():
    print("Start the test")
    c1 = Comment("This is a good answer", "VHS", datetime.datetime(2020, 5, 17))
    c2 = Comment("This is a bad answer", "VHS", datetime.datetime(2010, 5, 17))
    
    speakerFeature = Speaker_Feature()
    ret = speakerFeature.isSameSpeaker(c1, c2)
    assert ret, "Same author is not detected"
    
    c3 = Comment("+1 for the answer", "Jon Skeet", datetime.datetime(2015, 5, 17))
    ret = speakerFeature.isSameSpeaker(c1, c3)
    assert not ret, "Different author is not detected"
    
    print("End of the test")
    
testSameSpeaker()