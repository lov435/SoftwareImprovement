# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:19:54 2020

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from trainingdata.training_data import Training_Data
from features.semantic_feature import Semantic_Feature
# from features.bert_feature import Bert_Feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_recall_fscore_support
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
    
    def _getTrainingData(self, percent=1.0):
        assert percent <= 1.0 and percent >= 0.0
        d = Training_Data()
        all_posts = d.loadData()
        num_train = int(len(all_posts) * percent)
        return all_posts[:num_train],all_posts[num_train:]

    def _computeFeatures(self, all_posts):
        speaker_feature = Speaker_Feature()
        semantic_feature = Semantic_Feature()
        timeFeatures = Time_Features()
        textSimFeatures = Text_Similarity_Features()
        # bert_feature = Bert_Feature()

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

                x1 = int(speaker_feature.isSameSpeaker(comment1, comment2) == True)
                x2 = int(speaker_feature.refersToSpeakerUseCacheNoOrder(comment1, comment2) == True)
                #x2 = True
                x3 = semantic_feature.weighted_cosine_similarity(comment1, comment2)
                #x3 = 1

                feature_dict = timeFeatures.getTimeFeature(comment1, comment2)
                # x4 = feature_dict["tdiff_minute"]
                # x5 = feature_dict["tdiff_5min"]
                # x6 = feature_dict["tdiff_30min"]
                x7 = feature_dict["tdiff_hour"]
                x8 = feature_dict["tdiff_24h"]
                x9 = feature_dict["tdiff_week"]
                # x10 = feature_dict["tdiff_month"]
                # x11 = feature_dict["tdiff_half_year"]
                # x12 = feature_dict["tdiff_year"]
                x13 = feature_dict["other"]

                x14 = textSimFeatures.jaccard_feature(comment1, comment2)

                x15 = int(speaker_feature.refersToThirdSpeaker(comment1, comment2) == True)
                # x16 = bert_feature.cosine_similarity(comment1, comment2)

                features = [x1, x2, x3, x7, x8, x9, x13, x14, x15]
                print(features)
                X.append(features)
                Y.append(y)

        return X, Y


    def _checkFeatureImportance(self,model,X,Y):
        for feature in zip(self.feature_labels, model.feature_importances_):
            print(feature)


    def _printKeysAndPreds(self, predfile, keysfile, test_posts, proba):
        start = 0
        with open(predfile, 'w') as pf, open(keysfile, 'w') as kf:
            for t_post in test_posts:
                pairs = list(combinations(enumerate(t_post), 2))
                pairs_proba = sorted(zip(pairs, proba), key=lambda x: x[0][1])
                for (item1, item2), pr_tuple in pairs_proba:
                    kf.write(str(start + item2[0]) + " " + str(start + item1[0]) + "\n")
                    if (pr_tuple[0] > 0.5):
                        pf.write("0\t" + str(1 - pr_tuple[0]) + "\n")
                    else:
                        pf.write("1\t" + str(pr_tuple[1]) + "\n")
                start = start + len(t_post)
                #add a dummy link as E&C requires it
                kf.write(str(start) + " " + str(start-1) + "\n")
                pf.write("0\t0.0001\n")

    # def _printPredictions(self, predfile, proba):
    #     with open(predfile, 'w') as f:
    #         for pr_tuple in proba:
    #             if (pr_tuple[0] > 0.5):
    #                 f.write("0\t" + str(1 - pr_tuple[0]) + "\n")
    #             else:
    #                 f.write("1\t" + str(pr_tuple[1]) + "\n")
    #
    #
    # def _printKeys(self, keysfile, test_posts):
    #     start = 0
    #     with open(keysfile, 'w') as f:
    #         for t_post in test_posts:
    #             pairs = list(combinations(enumerate(t_post), 2))
    #             for (item1, item2) in pairs:
    #                 f.write(str(start + item2[0]) + " " + str(start + item1[0]) + "\n")
    #             start = start + len(t_post)


    def _printChats(self, chatsfile, test_posts):
        with open(chatsfile, 'w', encoding='utf-8') as f:
            idx = 1
            for t_post in test_posts:
                for comment in t_post.items():
                    name = comment[0].author.authorName.replace(" ", "_")
                    f.write("T1234 " + str(idx) + " u_" + name + " :  " + comment[0].text + "\n")
                    idx = idx + 1


    def runModelTrainTestSplit(self):
        train_posts, test_posts = self._getTrainingData(0.7)
        X, Y = self._computeFeatures(train_posts)

        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))

        model = RandomForestClassifier(n_estimators=500)
        model.fit(np.array(X), np.array(Y))
        TX, TY = self._computeFeatures(test_posts)
        pred_Y = model.predict(np.array(TX))

        print(precision_recall_fscore_support(TY, pred_Y))

        proba_Y = model.predict_proba(np.array(TX))
        print(proba_Y)

        for t_post in test_posts:
            pairs = list(combinations(t_post, 2))
            for i, (comment1, comment2) in enumerate(pairs):
                print(comment1.text)
                print(comment2.text)
                print(proba_Y[i][0])

        self._printChats('chats',test_posts)
        # self._printKeys('keys',test_posts)
        # self._printPredictions('predictions',proba_Y)
        self._printKeysAndPreds("predictions","keys",test_posts,proba_Y)



    def runModelCrossVal(self):
        train_posts, test_posts = self._getTrainingData()
        X, Y = self._computeFeatures(train_posts)
        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))
        
        # X_resampled, Y_resampled = SMOTE().fit_resample(np.array(X), np.array(Y))
        # print("Oversampled Y samples are ", sorted(Counter(Y_resampled).items()))

        model = RandomForestClassifier(max_depth=5)
        model.fit(np.array(X), np.array(Y))
        #self._checkFeatureImportance(model,X,Y)

        #model = KNeighborsClassifier(3)
        #model = SVC()

        #Let's do 10-Fold Cross validation
        print("Average cross validation accuracy is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring='accuracy')))

        print("Average cross validation F-measure is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring='f1')))  
        
        #Now let's run the classifier on SMOTE oversampled dataset
        # print("Average cross validation accuracy on oversampled dataset is")
        # print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='accuracy')))
        #
        # print("Average cross validation F-measure on oversampled dataset is")
        # print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='f1')))


if __name__ == '__main__':
    model = SO_Model()
    model.runModelCrossVal()
    #model.runModelTrainTestSplit()