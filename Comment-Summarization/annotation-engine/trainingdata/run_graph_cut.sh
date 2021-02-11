#!/bin/bash
  
export PYTHONHASHSEED=0
export PYTHONPATH=.
export PYTHONPATH=$PYTHONPATH:$PWD/../elsner-charniak-08-mod
export PYTHONPATH=$PYTHONPATH:$PWD/../elsner-charniak-08-mod/analysis
export PYTHONPATH=$PYTHONPATH:$PWD/../elsner-charniak-08-mod/utils
export PYTHONPATH=$PYTHONPATH:$PWD/../elsner-charniak-08-mod/viewer
export PATH=$PATH:$PWD/../elsner-charniak-08-mod/megam_0.92

python2.7 ../elsner-charniak-08-mod/model/greedy.py chats predictions keys > outchats 

