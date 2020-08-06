# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:44:27 2020

@author: viral
"""

import requests, sys
import time, csv

userdb = "Users cache.csv"

class Speaker_Feature:
    
    def __init__(self):
        self.cache = {}
    
    def isSameSpeaker(self, c1, c2):
        return c1.author == c2.author
    
    def _getPreviousNames(self, authorUid):
        #Sleep for a second. SO blocks us if too many requests are made in a second
        time.sleep(1)
        unames = []
        webapi = 'https://api.stackexchange.com/2.2/users/' + str(authorUid) + '/mentioned?page=1&pagesize=100&order=asc&sort=creation&site=stackoverflow.com&filter=!YOLt0NABWLb)BdLXdwgWbSTWPr&key=dgtaEQoc185ckdX2lTniJQ(('
        json_data = requests.get(webapi).json()
        #print(json_data)
        for item in json_data['items']:
            body = item['body']
            names = [ t for t in body.split() if t.startswith('@') ]
            if names:
                name = names[0][1:]
                if not name in unames:
                    unames.append(name)            
        return unames


    def _loadCache(self):
        with open(userdb, newline='', encoding="utf8", errors='ignore') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    self.cache[row[0].strip()] = row[1:]
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(userdb, reader.line_num, e))
    
    def _getPreviousNamesFromCache(self, authorUid):
        #Load user cache if it is empty
        if not self.cache:
           self. _loadCache()
           
        unames = self.cache[authorUid]
        
        return unames #if unames else self._getPreviousNames(authorUid)
        
    def _priorAuthorNameMentioned(self, text, authorUid, useCache):
        if useCache:
            unames = self._getPreviousNamesFromCache(authorUid)
        else:
            unames = self._getPreviousNames(authorUid)
        included = False
        for uname in unames:
            if "@" + str(uname) in text:
                included = True
                break
        return included
    
    def refersToSpeaker(self, c1, c2):
        return ("@" + c2.author.authorName in c1.text) or self._priorAuthorNameMentioned(c1.text, c2.author.authorId, False)
  
    def refersToSpeakerUseCache(self, c1, c2):
        return ("@" + c2.author.authorName in c1.text) or self._priorAuthorNameMentioned(c1.text, c2.author.authorId, True)

    def refersToSpeakerNoOrder(self, c1, c2):
        return self.refersToSpeaker(c1, c2) or self.refersToSpeaker(c2, c1)
    
    def refersToSpeakerUseCacheNoOrder(self, c1, c2):
        return self.refersToSpeakerUseCache(c1, c2) or self.refersToSpeakerUseCache(c2, c1)
    
    def refersToThirdSpeaker(self, c1, c2):
        sameThirdSpeaker = False
        c1mentions = [ t for t in c1.text.split() if t.startswith('@') ]
        c2mentions = [ t for t in c2.text.split() if t.startswith('@') ]
        if c1mentions and c2mentions:
            if c1mentions[0].lower() in c2mentions[0].lower() or \
            c2mentions[0].lower() in c1mentions[0].lower():
                sameThirdSpeaker = True
        return sameThirdSpeaker
            
            