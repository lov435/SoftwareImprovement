# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:56:12 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from trainingdata.training_data import Training_Data
from features.speaker_feature import Speaker_Feature

userdb = "Users cache.csv"


class SOUserCache:
    
    def writeCSV(self, lines):
        f = open(userdb, 'w', encoding="utf8", errors='ignore')
        for line in lines:
            f.write(line + '\n')
        f.close()
        
    def cacheUser(self):
        speaker_feature = Speaker_Feature()
        authors = set()
        d = Training_Data()
        all_posts = d.loadData()
        authors = {comment.author.authorId for post in all_posts for comment in post.keys()}
        authors.discard(0)
        authors - set([None])
        lines = []
                
        for author in authors:
            try:
                prevNames = speaker_feature._getPreviousNames(author)
                line = author + "," + ','.join(prevNames)
                lines.append(line)
            except Exception as e:
                print("Error occurred for author", author)
                print(str(e))
        
        self.writeCSV(lines)

cache = SOUserCache()
cache.cacheUser()