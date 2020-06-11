# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:52:58 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime
from general.comment import Comment
from general.author import Author
from features.speaker_feature import Speaker_Feature

def testSameSpeaker():
    print("Start the same speaker test")
    a1 = Author("VHS", 5749570, 8192)
    a2 = Author("VHS", 5749570, 8192)
    c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17))
    c2 = Comment("This is a bad answer", a2, datetime.datetime(2010, 5, 17))
    
    speakerFeature = Speaker_Feature()
    ret = speakerFeature.isSameSpeaker(c1, c2)
    assert ret, "Same author is not detected"
    
    a3 = Author("Jon Skeet", 22656, 1186748)
    c3 = Comment("+1 for the answer", a3, datetime.datetime(2015, 5, 17))
    ret = speakerFeature.isSameSpeaker(c1, c3)
    assert not ret, "Different author is not detected"
    
    print("End of the same speaker test")
    
def testRefersToSpeaker():
    print("Start the refers to speaker test")
    a1 = Author("VHS", 5749570, 8192)
    a2 = Author("Chux", 2410359, 99547)
    c1 = Comment("This is a good answer", a1, datetime.datetime(2020, 5, 17))
    c2 = Comment("Thanks @VHS. I appreciate it", a2, datetime.datetime(2010, 5, 17))
    
    speakerFeature = Speaker_Feature()
    ret = speakerFeature.refersToSpeaker(c2, c1)
    assert ret, "Refers to author not detected"
    
    a3 = Author("Jon Skeet", 22656, 1186748)
    c3 = Comment("+1 VHS for your answer", a3, datetime.datetime(2015, 5, 17))
    ret = speakerFeature.refersToSpeaker(c3, c1)
    assert not ret, "Refers to author shouldn't have been detected"
    
    c4 =  Comment("Thank you @ViralSheth. Glad to be of help", a3, datetime.datetime(2015, 5, 17))
    ret = speakerFeature.refersToSpeaker(c4, c1)
    assert ret, "Refers to author not detected"
        
    print("End of the refers to speaker test")
    
testSameSpeaker()
testRefersToSpeaker()