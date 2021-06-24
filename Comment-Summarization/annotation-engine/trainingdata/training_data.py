# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:24:14 2020

@author: viral
"""

import csv, sys, datetime, copy
from general.comment import Comment
from general.author import Author

enrichedFile = "Enriched annotations.csv"

class Training_Data:
    def loadData(self):
        with open(enrichedFile, newline='', encoding="utf8", errors='ignore') as f:
            reader = csv.reader(f)
            all_posts = [] #list of post that has comments and groups
            post_comments = {} #all comments of a post and their groups
            url=''
            try:
                for row in reader:
                    #If we have the comment from the 3rd column, take that because it is from SO API
                    if not row[2].strip() == '':
                        text = row[2]
                    else:
                        text = row[1]
                        #Take the text only up to the en dash character
                        text = text[:text.index(u"\u2013")]
                    #Restore the original comma    
                    text = text.replace("|COMMA|", ",")
                    
                    timestamp = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                    
                    #Author info
                    uid = row[4]
                    uname = row[5]
                    reputation = row[6]                    
                    author = Author(uname, uid, reputation)
                    upvotes = row[8]
                    
                    comment = Comment(text, author, timestamp, upvotes)

                    group = row[7]
                    
                    if not row[0].strip() == url:
                        if post_comments: #if the dict is not empty
                            all_posts.append(copy.deepcopy(post_comments))
                        post_comments.clear()
                        url = row[0].strip()
                        
                    post_comments[comment] = group
                    
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(enrichedFile, reader.line_num, e))
            
            #Add the last comment rating dictionary to the list
            all_posts.append(copy.deepcopy(post_comments))

            return all_posts

d = Training_Data()
posts = d.loadData()