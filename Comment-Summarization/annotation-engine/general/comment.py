# -*- coding: utf-8 -*-
"""
Created on Wed May 21 23:37:10 2020

@author: viral
"""

class Comment:
    def __init__(self, text, author, timeStamp, upvotes=0):
        self.text = text
        self.author = author
        self.timeStamp = timeStamp
        self.upvotes = upvotes
