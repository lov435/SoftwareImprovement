# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:08:50 2020

@author: viral
"""

import csv, sys, requests, datetime
from general.comment import Comment
from general.author import Author

csvFile = "Merged annotations - Comments.csv"
enrichedFile = "Enriched annotations.csv"

class Enrichment:
    
    def retrieveComments(self, ansId):
        webapi = 'https://api.stackexchange.com/2.2/answers/' + str(ansId) + '/comments?page=1&pagesize=100&order=asc&sort=creation&site=stackoverflow&key=aT0javmxqIqcfwsWoTDA4w((&filter=!)srVqBhiaSgtcRgeozZw'
        json_data = requests.get(webapi).json()
        #print(json_data)
        comments = []
        for item in json_data['items']:
            #print(item)
            owner = item['owner']
            uname = owner['display_name']
            if 'user_id' in owner: #If the user is not deleted from SO
                uid = owner['user_id']
                reputation = owner['reputation']
            else:
                uid = None
                reputation = 0
            
            author = Author(uname, uid, reputation)
            text = item['body']
            epochTime = item['creation_date']
            timestamp = datetime.datetime.fromtimestamp(epochTime).strftime('%Y-%m-%d %H:%M:%S')
            comment = Comment(text, author, timestamp)
            comments.append(comment)
        return comments
    
    def _getCommentWithText(self, comments, text):
        blankAuthor = Author('', 0, 0)
        match = Comment('', blankAuthor, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for comment in comments:
            set1 = set()
            set1.update(word for word in text.strip().split())
            len1 = len(set1)
            set2 = set()
            set2.update(w for w in comment.text.strip().split())
            len2 = len(set2)
            
            both = set1 | set2
            lenboth = len(both)
            #If most of the words are common, it's the same comment
            if lenboth < 1.25*len1 and lenboth < 1.25*len2:
                match = comment
                break
        return match
    
    def writeCSV(self, lines):        
        #with open(enrichedFile, "w", encoding="utf8", errors='ignore') as csv_file:
        #    writer = csv.writer(csv_file, delimiter=',')
        #    for line in lines:
        #        writer.writerow(line)
        f = open(enrichedFile, 'w', encoding="utf8", errors='ignore')
        for line in lines:
            f.write(line + '\n')
        f.close()
                
    def enrichCSV(self):
        lines = []
        with open(csvFile, newline='', encoding="utf8", errors='ignore') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            try:
                for row in reader:
                    comment = row[1]
                    group = row[2]
                    
                    if not row[0].strip() == '':
                        url = row[0]
                        words = url.split("/")
                        answerId = words[4]
                        comments = self.retrieveComments(answerId)
                        
                    matched_comment = self._getCommentWithText(comments, comment[:comment.index(u"\u2013")])
                    line = url + "," + comment.replace(",", "|COMMA|") + "," + matched_comment.text.replace(",", "|COMMA|") + "," + \
                    matched_comment.timeStamp + "," + str(matched_comment.author.authorId) + "," + \
                    matched_comment.author.authorName + "," + str(matched_comment.author.repPoints) + "," + str(group)
                    lines.append(line)
                    
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(csvFile, reader.line_num, e))
        
        self.writeCSV(lines)
                
enrichment = Enrichment()
enrichment.enrichCSV()