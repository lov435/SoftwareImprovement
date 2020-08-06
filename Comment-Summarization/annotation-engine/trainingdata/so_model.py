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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from imblearn.over_sampling import SMOTE, ADASYN

from features.speaker_feature import Speaker_Feature
from features.time_features import Time_Features
from features.text_similarity_features import Text_Similarity_Features

from itertools import combinations
from collections import Counter

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
        textSimFeatures = Text_Similarity_Features()

        X = []
        Y = []
        self.feature_labels = ["same_speaker","refers_to_speaker","semantic_cos",
            "tdiff_minute","tdiff_5min","tdiff_30min","tdiff_hour","tdiff_24h",
            "tdiff_week","tdiff_month","tdiff_half_year","tdiff_year","other", 
            "jaccard", "refers_to_third_speaker"]

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
                    x3 = semantic_feature.cosine_similarity(comment1, comment2)
                    #x3 = 1
                            
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
                    
                    x14 = textSimFeatures.jaccard_feature(comment1, comment2)
                    
                    x15 = speaker_feature.refersToThirdSpeaker(comment1, comment2)


                    features = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15]                
                    X.append(features) 
                    Y.append(y)
                except Exception as e:
                    print("-----")
                    print(comment1.text)
                    print(comment2.text)
                    print("Skipping this comment pair for an error: " + str(e))

        return X, Y


    def _checkFeatureImportance(self,model,X,Y):
        for feature in zip(self.feature_labels, model.feature_importances_):
            print(feature)


    def trainModel(self):
        X, Y = self._getTrainingData()
        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))
        
        X_resampled, Y_resampled = SMOTE().fit_resample(np.array(X), np.array(Y))
        print("Oversampled Y samples are ", sorted(Counter(Y_resampled).items()))

        #model = RandomForestClassifier(max_depth=5)
        #model.fit(np.array(X), np.array(Y))
        #self._checkFeatureImportance(model,X,Y)

        #model = KNeighborsClassifier(3)

        model = SVC()

        #Let's do 10-Fold Cross validation
        print("Average cross validation accuracy is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring='accuracy')))        

        print("Average cross validation F-measure is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring='f1')))  
        
        #Now let's run the classifier on SMOTE oversampled dataset
        print("Average cross validation accuracy on oversampled dataset is")
        print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='accuracy')))        

        print("Average cross validation F-measure on oversampled dataset is")
        print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='f1')))        


if __name__ == '__main__':
    model = SO_Model()
    model.trainModel()