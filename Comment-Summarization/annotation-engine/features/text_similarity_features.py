# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:57:16 2020

@author: viral
"""

import nltk
import re
from nltk.stem import WordNetLemmatizer 

class Text_Similarity_Features:
    
    def _lemmatize(self, text):
        # Init the Wordnet Lemmatizer
        lemmatizer = WordNetLemmatizer()
        # Tokenize: Split the sentence into words
        word_list = nltk.word_tokenize(text)
        return [lemmatizer.lemmatize(w) for w in word_list]

    def _filtercamelcase(self, text):
        pattern = '[A-Z]+[a-z0-9]+[A-Z]+[a-z0-9]+'
        return re.findall(pattern,text)

    def jaccard_feature(self, comment1, comment2):
        bow1 = self._lemmatize(comment1.text)
        bow2 = self._lemmatize(comment2.text)
        intersection = set(bow1).intersection(set(bow2))
        union = set(bow1).union(set(bow2))
        return len(intersection)/len(union)

    def jaccard_code_feature(self, comment1, comment2):
        bow1 = self._filtercamelcase(comment1.text)
        bow2 = self._filtercamelcase(comment2.text)
        intersection = set(bow1).intersection(set(bow2))
        union = set(bow1).union(set(bow2))
        if len(union) == 0:
            return 0
        else:
            return len(intersection)/len(union)