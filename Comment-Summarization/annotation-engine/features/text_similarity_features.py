# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:57:16 2020

@author: viral
"""

import nltk
from nltk.stem import WordNetLemmatizer 

class Text_Similarity_Features:
    
    def _lemmatize(self, text):
        # Init the Wordnet Lemmatizer
        lemmatizer = WordNetLemmatizer()
        # Tokenize: Split the sentence into words
        word_list = nltk.word_tokenize(text)
        return [lemmatizer.lemmatize(w) for w in word_list]

    def jaccard_feature(self, comment1, comment2):
        bow1 = self._lemmatize(comment1.text)
        bow2 = self._lemmatize(comment2.text)
        intersection = set(bow1).intersection(set(bow2))
        union = set(bow1).union(set(bow2))
        return len(intersection)/len(union)
