# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:19:54 2020

@author: viral
"""

import sys, os

THRESHOLD_FOR_CLUSTERING = 0.4
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from trainingdata.training_data import Training_Data
from features.semantic_feature import Semantic_Feature
# from features.bert_feature import Bert_Feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_recall_fscore_support, make_scorer, f1_score, \
    accuracy_score, precision_score, recall_score, roc_auc_score

from sklearn.model_selection import RepeatedStratifiedKFold

from features.speaker_feature import Speaker_Feature
from features.time_features import Time_Features
from features.text_similarity_features import Text_Similarity_Features

from xgboost import XGBClassifier

from itertools import combinations
from collections import Counter

import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential

from lightgbm import LGBMClassifier

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
        self.feature_labels = []

        # use_features = ['semantic']
        use_features = ['speaker', 'time', 'text_similarity', 'semantic']

        for post in all_posts:
            pairs = list(combinations(post, 2))
            for (comment1, comment2) in pairs:
                group1 = post.get(comment1)
                group2 = post.get(comment2)
                y = 1 if group1 == group2 else 0

                features = []
                if 'speaker' in use_features:
                    x1 = int(speaker_feature.isSameSpeaker(comment1, comment2) == True)
                    x2 = int(speaker_feature.refersToSpeakerUseCacheNoOrder(comment1, comment2) == True)
                    x16 = int(speaker_feature.refersToSameThirdSpeaker(comment1, comment2) == True)
                    x21 = int(speaker_feature.refersToDifferentThirdSpeaker(comment1, comment2) == True)
                    features.extend([x1,x2,x16,x21])
                    self.feature_labels.extend(["same_speaker","refers_to_speaker","refers_to_same_speaker","refers_to_diff_speaker"])

                if 'semantic' in use_features:
                    x3 = semantic_feature.weighted_cosine_similarity(comment1, comment2)
                    x4 = semantic_feature.cosine_similarity(comment1, comment2)
                    features.extend([x3,x4])
                    self.feature_labels.extend(["weighted_cosine","cosine"])

                if 'time' in use_features:
                    feature_dict = timeFeatures.getTimeFeature(comment1, comment2)
                    x5 = feature_dict["tdiff_5min"]
                    x7 = feature_dict["tdiff_hour"]
                    x8 = feature_dict["tdiff_24h"]
                    x9 = feature_dict["tdiff_week"]
                    x13 = feature_dict["other"]
                    features.extend([x5,x7,x8,x9,x13])
                    self.feature_labels.extend(["tdiff_5min","tdiff_hour","tdiff_24h","tdiff_week","tdiff_other"])

                if 'text_similarity' in use_features:
                    x14 = textSimFeatures.jaccard_feature(comment1, comment2)
                    x15 = textSimFeatures.jaccard_code_feature(comment1, comment2)
                    features.extend([x14,x15])
                    self.feature_labels.extend(["jaccard","jaccard_code"])

                # x16 = bert_feature.cosine_similarity(comment1, comment2)

                #print(features)
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
                    if (pr_tuple[0] > THRESHOLD_FOR_CLUSTERING):
                        pf.write("0\t" + str(1 - pr_tuple[0]) + "\n")
                    else:
                        pf.write("1\t" + str(pr_tuple[1]) + "\n")
                start = start + len(t_post)
                #add a dummy link as E&C requires it
                kf.write(str(start) + " " + str(start-1) + "\n")
                pf.write("0\t0.0001\n")


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

        model = RandomForestClassifier(max_depth=5)
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
        self._printKeysAndPreds("predictions","keys",test_posts,proba_Y)


    def runModelNeuralNet(self):
        train_posts, test_posts = self._getTrainingData(0.7)
        X, Y = self._computeFeatures(train_posts)
        TX, TY = self._computeFeatures(test_posts)
        #Convert the list of list to 2d numpy array
        X = np.array(X)
        TX = np.array(TX)
        #Convert the booleans to ints
        X = np.multiply(X, 1)
        TX = np.multiply(TX, 1)
        #Convert the list to a 1d numpy array
        Y = np.array(Y)
        TY = np.array(TY)
        
        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))
        
        #Define the model
        model = Sequential()
        model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_dim=X.shape[1]))
        model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
        model.add(Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer='adam', loss='binary_crossentropy', 
                       metrics=['accuracy', 
                                tf.keras.metrics.Precision(name='precision'),
                                tf.keras.metrics.Recall(name='recall')])
        # fit the model
        history = model.fit(X, Y, epochs=1500, batch_size=32, verbose=0)
        accuracy = history.history['accuracy'][-1]
        precision = history.history['precision'][-1]
        recall = history.history['recall'][-1]
        f_measure = 2*((precision*recall)/(precision+recall))
        print('Train accuracy is ', accuracy)
        print('Train f_measure is ', f_measure)
        
        scores = model.evaluate(TX, TY)
        print("%s:-> %.2f%%" % (model.metrics_names[1], scores[1]))
        print("The test f_measure is ", 2*((scores[2]*scores[3])/(scores[2]+scores[3])))


    def runModelCrossVal(self):
        train_posts, test_posts = self._getTrainingData()
        X, Y = self._computeFeatures(train_posts)
        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))
        
        # X_resampled, Y_resampled = SMOTE().fit_resample(np.array(X), np.array(Y))
        # print("Oversampled Y samples are ", sorted(Counter(Y_resampled).items()))

        # model = KNeighborsClassifier(3)
        # model = SVC()
        model = RandomForestClassifier(max_depth=5)
        # model.fit(np.array(X), np.array(Y))
        # self._checkFeatureImportance(model,X,Y)


        #Let's do 10-Fold Cross validation
        print("Average cross validation accuracy is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring='accuracy')))

        scorer = make_scorer(f1_score, average='micro')
        print("Average cross validation F-measure is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(precision_score)
        print("Average cross validation precision is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(recall_score)
        print("Average cross validation recall is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(roc_auc_score)
        print("Average cross validation ROC AUC is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        #Now let's run the classifier on SMOTE oversampled dataset
        # print("Average cross validation accuracy on oversampled dataset is")
        # print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='accuracy')))
        #
        # print("Average cross validation F-measure on oversampled dataset is")
        # print(np.mean(cross_val_score(model, X_resampled, Y_resampled, cv=10, scoring='f1')))

    def runSimpleBaselines(self):
        train_posts, test_posts = self._getTrainingData()
        X, Y = self._computeFeatures(train_posts)
        print("Size of Training set is", len(X), len(Y))
        print("Y samples are ", sorted(Counter(np.array(Y)).items()))

        #column 1 = refers to speaker
        predi = [row[1] for row in X]

        res = precision_recall_fscore_support(Y,predi,average='micro')
        print("Average cross validation precision is")
        print(precision_score(Y,predi,average='micro'))
        print("Average cross validation recall is")
        print(res[1])
        print("Average cross validation F-score is")
        print(res[2])

    def runModelCrossValXGBoost(self):
        train_posts, test_posts = self._getTrainingData()
        X, Y = self._computeFeatures(train_posts)

        #Construct the XGBoost classifer model
        #Specify these 2 parameters to constructor to avoid warnings
        model = XGBClassifier(eval_metric='logloss', use_label_encoder=False)
        
        scorer = make_scorer(f1_score, average='micro')
        print("Average cross validation F-measure is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(precision_score)
        print("Average cross validation precision is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(recall_score)
        print("Average cross validation recall is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

        scorer = make_scorer(roc_auc_score)
        print("Average cross validation ROC AUC is")
        print(np.mean(cross_val_score(model, np.array(X), np.array(Y), cv=10, scoring=scorer)))

    def runModelCrossValLightGBM(self):
        train_posts, test_posts = self._getTrainingData()
        X, Y = self._computeFeatures(train_posts)

        model = LGBMClassifier()
        #cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

        print("Average cross validation accuracy is")
        print(np.mean(cross_val_score(model,  np.array(X), np.array(Y), scoring='accuracy', cv=10)))
        
        scorer = make_scorer(f1_score, average='micro')
        print("Average cross validation F-measure is")
        print(np.mean(cross_val_score(model,  np.array(X), np.array(Y), scoring=scorer, cv=10)))

        scorer = make_scorer(precision_score)
        print("Average cross validation precision is")
        print(np.mean(cross_val_score(model,  np.array(X), np.array(Y), scoring=scorer, cv=10)))

        scorer = make_scorer(recall_score)
        print("Average cross validation recall is")
        print(np.mean(cross_val_score(model,  np.array(X), np.array(Y), scoring=scorer, cv=10)))


if __name__ == '__main__':
    model = SO_Model()
    model.runModelCrossVal() #Random Forest is the best of all
    #model.runModelCrossValXGBoost()
    #model.runModelCrossValLightGBM()
    # model.runModelTrainTestSplit()
    # model.runModelNeuralNet()
    # model.runSimpleBaselines()
