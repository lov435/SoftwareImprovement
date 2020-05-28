# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:44:27 2020

@author: viral
"""

class Speaker_Feature:
    def isSameSpeaker(self, c1, c2):
        return c1.authorId == c2.authorId