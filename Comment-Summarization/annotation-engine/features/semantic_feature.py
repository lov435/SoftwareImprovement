# -*- coding: utf-8 -*-
"""
Created on ...

@author: damevski
"""

import numpy as np
import scipy
import os
import gensim
from gensim.scripts.glove2word2vec import glove2word2vec

class Semantic_Feature:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        embedding_file = os.path.join(script_dir, 'embeddings/vectors.txt')
        w2v_embedding_file = os.path.join(script_dir, 'embeddings/w2v_vectors.txt')
        if not os.path.exists(w2v_embedding_file):
            glove2word2vec(embedding_file, w2v_embedding_file)
        self.model = gensim.models.KeyedVectors.load_word2vec_format(w2v_embedding_file)
    
    def cosine_similarity(self, c1, c2):
        c1_words = [word for word in c1.text.split() if word in self.model.vocab]
        if not c1_words:
            return 0.0
        mean_vec_c1 = np.mean(self.model[c1_words], axis=0)
        c2_words = [word for word in c2.text.split() if word in self.model.vocab]
        if not c2_words:
            return 0.0
        mean_vec_c2 = np.mean(self.model[c2_words], axis=0)
        cosine = 1.0 - scipy.spatial.distance.cosine(mean_vec_c1, mean_vec_c2)
        return cosine