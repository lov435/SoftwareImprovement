# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:19:54 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from trainingdata.training_data import Training_Data
from features.semantic_feature import Semantic_Feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from features.speaker_feature import Speaker_Feature
from features.time_features import Time_Features
from itertools import combinations
import numpy as np

class SO_Model:
    
    def _getAllCommments(self, posts):
        comments = []
        for post in posts:
            comments = comments + list(post.keys())
        return comments
    
    def _getTrainingData(self):
        d = Training_Data()
        all_posts = d.loadData()
        
        speaker_feature = Speaker_Feature()
        semantic_feature = Semantic_Feature()
        timeFeatures = Time_Features()
        X = []
        Y = []
        
        for post in all_posts:
            pairs = list(combinations(post, 2))
            for (comment1, comment2) in pairs:
                group1 = post.get(comment1)
                group2 = post.get(comment2)
                y = 1 if group1 == group2 else 0
                try:
                    x1 = speaker_feature.isSameSpeaker(comment1, comment2)
                    x2 = speaker_feature.refersToSpeakerUseCacheNoOrder(comment1, comment2)
                    #x2 = True
                    #x3 = semantic_feature.cosine_similarity(comment1, comment2)
                    x3 = 1                    
                            
                    feature_dict = timeFeatures.getTimeFeature(comment1, comment2)
                    x4 = feature_dict["tdiff_minute"]
                    x5 = feature_dict["tdiff_5min"]
                    x6 = feature_dict["tdiff_30min"]
                    x7 = feature_dict["tdiff_hour"]
                    x8 = feature_dict["tdiff_24h"]
                    x9 = feature_dict["tdiff_week"]
                    x10 = feature_dict["tdiff_month"]
                    x11 = feature_dict["tdiff_half_year"]
                    x12 = feature_dict["tdiff_year"]
                    x13 = feature_dict["other"]
                    
                    features = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13]                
                    X.append(features) 
                    Y.append(y)
                except:
                    print(comment1.text)
                    print("-----")
                    print(comment2.text)
                    print("Skipping this comment pair for an error")            
        return X, Y
        
        
    def trainModel(self):
        X, Y = self._getTrainingData()
        print("Size of Training set is", len(X), len(Y))
        model = RandomForestClassifier(n_estimators=40)
        #model.fit(np.array(X), np.array(Y))
        
        #Let's do 10-Fold Cross validation
        print("Average cross validation score is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10)))        

model = SO_Model()
model.trainModel()