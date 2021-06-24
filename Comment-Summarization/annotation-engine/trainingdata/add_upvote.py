# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 23:32:39 2021

This script takes the comment upvotes column from the new enrichment csv
and adds it to the existing enrichment csv as the last column. Instead of 
using the new enrichment csv, we are using the old one because, the new one
doesn't have many comments which are now deleted in StackOverflow

@author: viral
"""

import pandas as pd

enrichedFile = "Enriched annotations.csv"
upvoteFile = "new_Enriched annotations.csv"

csv_input = pd.read_csv(enrichedFile, header=None)
upvote_input = pd.read_csv(upvoteFile, header=None)
csv_input[8] = upvote_input[8]
csv_input.to_csv(enrichedFile, index=False, header=None)