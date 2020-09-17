# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:38:57 2020

@author: viral
"""

import scipy
import scipy.spatial
from bert_serving.client import BertClient

class Bert_Feature:
         
    def cosine_similarity(self, c1, c2):        
       #bc = BertClient(check_length=False)
       bc = BertClient()
       vectors = bc.encode([c1.text, c2.text])
       cosine = 1.0 - scipy.spatial.distance.cosine(vectors[0], vectors[1])
       return cosine
      