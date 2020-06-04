# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:44:27 2020

@author: viral
"""

import requests

class Speaker_Feature:
    def isSameSpeaker(self, c1, c2):
        return c1.author == c2.author
    
    def _getPreviousNames(self, authorUid):
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
    
    def _priorAuthorNameMentioned(self, text, authorUid):
        unames = self._getPreviousNames(authorUid)
        included = False
        for uname in unames:
            if "@" + str(uname) in text:
                included = True
                break
        return included
    
    def refersToSpeaker(self, c1, c2):
        return ("@" + c2.author.authorName in c1.text) or self._priorAuthorNameMentioned(c1.text, c2.author.authorId)