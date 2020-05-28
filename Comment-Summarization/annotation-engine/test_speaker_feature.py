# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:52:58 2020

@author: viral
"""

import datetime
from general.comment import Comment
from features.speaker_feature import Speaker_Feature

def testSameSpeaker():
    print("Start the same speaker test")
    c1 = Comment("This is a good answer", "VHS", datetime.datetime(2020, 5, 17))
    c2 = Comment("This is a bad answer", "VHS", datetime.datetime(2010, 5, 17))
    
    speakerFeature = Speaker_Feature()
    ret = speakerFeature.isSameSpeaker(c1, c2)
    assert ret, "Same author is not detected"
    
    c3 = Comment("+1 for the answer", "Jon Skeet", datetime.datetime(2015, 5, 17))
    ret = speakerFeature.isSameSpeaker(c1, c3)
    assert not ret, "Different author is not detected"
    
    print("End of the same speaker test")
    
def testRefersToSpeaker():
    print("Start the refers to speaker test")
    c1 = Comment("This is a good answer", "VHS", datetime.datetime(2020, 5, 17))
    c2 = Comment("Thanks @VHS. I appreciate it", "Chux", datetime.datetime(2010, 5, 17))
    
    speakerFeature = Speaker_Feature()
    ret = speakerFeature.refersToSpeaker(c2, c1)
    assert ret, "Refers to author not detected"
    
    c3 = Comment("+1 VHS for your answer", "Jon Skeet", datetime.datetime(2015, 5, 17))
    ret = speakerFeature.refersToSpeaker(c3, c1)
    assert not ret, "Refers to author shouldn't have been detected"
        
    print("End of the refers to speaker test")
    
testSameSpeaker()
testRefersToSpeaker()