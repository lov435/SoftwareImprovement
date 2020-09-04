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
        self.empty_vec_sim = 0.01
    
    def cosine_similarity(self, c1, c2):
        c1_words = [word for word in c1.text.split() if word in self.model.vocab]
        if not c1_words:
            return self.empty_vec_sim
        mean_vec_c1 = np.mean(self.model[c1_words], axis=0)
        c2_words = [word for word in c2.text.split() if word in self.model.vocab]
        if not c2_words:
            return self.empty_vec_sim
        mean_vec_c2 = np.mean(self.model[c2_words], axis=0)
        cosine = 1.0 - scipy.spatial.distance.cosine(mean_vec_c1, mean_vec_c2)
        return cosine

    def weighted_cosine_similarity(self, c1, c2):
        weighted_c1 = 0
        weighted_c2 = 0
        c1_words = [word for word in c1.text.split() if word in self.model.vocab]
        if not c1_words:
            return self.empty_vec_sim
        c2_words = [word for word in c2.text.split() if word in self.model.vocab]
        if not c2_words:
            return self.empty_vec_sim
        for c1_word in c1_words:
            weighted_c1 = np.add(weighted_c1, self.model[c1_word] * (0.001 / (0.001 + self.model.vocab[c1_word].count)))
        weighted_c1 = weighted_c1 / len(c1_words)
        for c2_word in c2_words:
            weighted_c2 = np.add(weighted_c2, self.model[c2_word] * (0.001 / (0.001 + self.model.vocab[c2_word].count)))
        weighted_c2 = weighted_c2 / len(c2_words)
        cosine = 1.0 - scipy.spatial.distance.cosine(weighted_c1, weighted_c2)
        return cosine
