# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:23:23 2020

@author: viral
"""

class Time_Features:

    def getTimeFeature(self, c1, c2):
        features = {
            "tdiff_minute" : 0,
            "tdiff_5min" : 0,
            "tdiff_30min" : 0,
            "tdiff_hour" : 0,
            "tdiff_24h" : 0,
            "tdiff_week" : 0,
            "tdiff_month" : 0,
            "tdiff_half_year" : 0,
            "tdiff_year" : 0,
            "other" : 0
            }
        
        t1 = c1.timeStamp
        t2 = c2.timeStamp
        
        if t1 < t2:
            duration = t2 - t1
        else:
            duration = t1 - t2
          
        secs = duration.total_seconds() 
        
        # if secs < 60: #1 minute
        #     features["tdiff_minute"] = 1
        # elif secs < 60*5: #5 minutes
        #     features["tdiff_5min"] = 1
        # elif secs < 60*30: #30 minutes
        #     features["tdiff_30min"] = 1
        if secs < 60*60: #an hour
            features["tdiff_hour"] = 1
        elif secs < 60*60*24: #24 hours
            features["tdiff_24h"] = 1
        elif secs < 60*60*24*7: #a week
            features["tdiff_week"] = 1
        # elif secs < 60*60*24*30: #a month (30 days)
        #     features["tdiff_month"] = 1
        # elif secs < 60*60*24*30*6: #6 months (180 days)
        #     features["tdiff_half_year"] = 1
        # elif secs < 60*60*24*365: #a year (365 days)
        #     features["tdiff_year"] = 1
        else: #the diff is more than a year
            features["other"] = 1
            
        return features