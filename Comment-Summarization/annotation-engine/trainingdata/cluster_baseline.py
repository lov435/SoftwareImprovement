# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 16:45:29 2021

@author: viral
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from trainingdata.training_data import Training_Data

baselineFile = "baseline_outchats_full"
group = 1

class Cluster_Baseline:
    
    def _getTrainingData(self):
        d = Training_Data()
        all_posts = d.loadData()
        return all_posts
    
    def insertToTopFive(self, topFive, comment):
        if len(topFive) == 0:
            topFive.append(comment)
            return
        else:
            index = len(topFive)
            for c in topFive:
                if (comment.upvotes > c.upvotes or 
                        (comment.upvotes == c.upvotes and
                         comment.timeStamp > c.timeStamp)):
                    index = topFive.index(c)
                    break
            topFive.insert(index, comment)
        
    def updateTopFive(self, topFive, comment):
        index = -1
        for c in topFive:
            if (comment.upvotes > c.upvotes or 
                    (comment.upvotes == c.upvotes and
                     comment.timeStamp > c.timeStamp)):
                index = topFive.index(c)
                break
        if index != -1:
            topFive.insert(index, comment)
            del topFive[-1] #remove the last element
            
    def writeOutchats(self, lines):        
        f = open(baselineFile, 'w', encoding="utf8", errors='ignore')
        for line in lines:
            f.write(line + '\n')
        f.close()
        
    def decideGroup(self, post_dict):
        global group
        topFive = [] #A list to hold top 5 comments per SO's algorithm       
        for comment in post_dict:
            if len(topFive) < 5:    
                self.insertToTopFive(topFive, comment)
            else:
                self.updateTopFive(topFive, comment)   
        
        lines = []
        for comment in post_dict:
            if comment in topFive:
                tid = "T" + str(group)
            else:
                tid = "T" + str(group + 1)
            line = tid + " 0 u_" + comment.author.authorName + " : " + comment.text
            lines.append(line)

        group = group + 2 #increment the group by 2
        return lines
    
    def main(self):
        all_lines = []
        all_posts = self._getTrainingData()
        for post in all_posts:
            lines = self.decideGroup(post)    
            all_lines.extend(lines)
                    
        self.writeOutchats(all_lines)

baseline = Cluster_Baseline()
baseline.main()