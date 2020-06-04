# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:34:25 2020

@author: viral
"""

class Author:
    def __init__(self, authorName, authorId, repPoints):
        self.authorName = authorName
        self.authorId = authorId
        self.repPoints = repPoints
        
    def __eq__(self, other): 
        if not isinstance(other, Author):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.authorName == other.authorName and self.authorId == other.authorId