=========================================
Chat Disentanglement
=========================================

.. contents::

Introduction
------------

This is the dataset and code described in [ElsnerCharniak08]_ . It is
designed to analyze IRC chat conversations, with the aim of
disentangling multiple simultaneous conversations.

:Contact:
	Micha Elsner (melsner@cs.brown.edu)

Some of the code in this package is written by other people.

:Other authors:
	   grouper.py (python cookbook)

	   AIMA utilities (support code for AI: A Modern Approach;
	   http://aima.cs.berkeley.edu/python/readme.html)

	   waterworks utility package (David McClosky; http://cs.brown.edu/~dmcc)

	   Probably/ClusterMetrics utilities (David McClosky; not
	   publically available yet)
	   
	   pyung.py Hungarian algorithm implementation (Federico
	   Tomassini)

:To make the code work, you will also need to download some programs:
	[megam]_, a maximum-entropy classifier by Hal Daume III

	pylab plotting library, which in turn needs [matplotlib]_ 
	(needed only for analysis programs which make diagrams)

Add the *utils* directory, which contains some general-purpose
libraries, to your PYTHONPATH environment variable.

Dataset
-------

The transcript is a recording from IRC, in late May 2007. It comes
from the ##linux channel at http://freenode.net. You can see a usage
profile of this channel at
http://irc.netsplit.de/channels/details.php?room=%23%23linux&net=freenode.

Ethics
======

The Brown IRB has determined that our study "does not involve the use
of human subjects as defined by the Code of Federal Regulations",
since it is not "about" the individuals in the chat room (presumably
because it does not use "private identifiable data").

However, we did feel it was appropriate to anonymize the chat as much
as possible, so we assigned each commentator an alias. These aliases
are randomly selected from a US Census name list (included as
*data/names*). Name substitution is not perfect; the system can't
detect misspelled or abbreviated names.

Data Files
==========

The dataset is contained in *IRC*. There are three annotated sections,
*IRC/test*, *IRC/pilot* and *IRC/dev*. In addition, there is the whole
dataset, *IRC/linux*, and all the unannotated data, *IRC/rest*.

The data is divided as follows:

	1-500: pilot (markable lines 359: 0:58:10)

	501-1501: dev (markable lines 706: 2:6:24)

	100 line gap, since the same annotators may mark both dev and test and we don't want them to make test decisions based on remembered dev data

	1601-2601: test (markable lines 800: 1:39:37)

	100 line gap

	rest

Currently we have four pilot annotations:

        pilot-0X (experimenter)

        1-2 (subjects)

        3X (subject, unfamiliar with linux OS)

One dev annotation:

        dev-0X (experimenter)

7 test annotations:

        0-5 (subjects)

        6X (subject, misunderstood instructions)

For linux-test-5.annot, a bug in the annotation software allowed the
annotation -1 (SYS_THREAD) for real lines. The lines which were
mislabeled were replaced with sequential annotations T70 through
T85. I have listed these here (by line number).

::

	 6 T-1 15423 Chauncey: the human touch ?
	 278 T-1 17586 Felicia: her*
	 409 T-1 18196 Inez: call later in the afternoon, since I sleep in late~
	 495 T-1 18646 Lai: Alisa: heh
	 646 T-1 19400 Lai: thanks
	 657 T-1 19452 Lai: Felicia:
	 665 T-1 19526 Nicki: why do you say "alleged" non-payment? did you pay or didn't you? :)
	 666 T-1 19528 Felicia: Lai: PM me the address .. atleast one of us will have it
	 687 T-1 19693 Felicia: hehe .. figures
	 721 T-1 20016 Arlie: congratulations
	 791 T-1 20388 Madison: tampa
	 795 T-1 20407 Alisa: Arlie: there are some nice coal fires in China too....maybe there.
	 857 T-1 20627 Mellisa: awww
	 908 T-1 20905 Santo: yay for romance languages
	 909 T-1 20909 Madison: lol
	 911 T-1 20912 Madison: you like ?


Format
======

For privacy and convenience, the chats have been edited so that each
line conforms to the following format:

::

	 time name (: comment)|(* action)

Times are given in seconds after the start of the transcript.

The name is the name of the speaker.

A comment is something someone "says"; an action is either a
system-generated message ("Matilda * entered the room") or a person's
action, shown in the third-person  ("Matilda * slaps Morris with a
trout").

Annotated lines have an additional field showing the thread:

::

	T(thread) time name (: comment)|(* action)

T-1 is the "system" thread, reserved for system messages. We recognize
four of these:

::

	 entered the room
	 left the room
	 set mode
	 is now known as

The namechange action ("foo is now known as bar") is rendered
meaningless by the aliasing system, since the old and new nicknames
are given the same alias ("Matilda * is now known as Matilda").

Preprocess and Annotation
-------------------------

We recorded our data using the gaim chat client. (gaim, now called
pidgin, is available from http://www.pidgin.im/) You can activate
logging from the *Tools/Preferences* menu item; click the *Logging*
tab, select "Plain text" logs and click "Log all chats".

The raw data can be formatted using the *preprocess/stripChat.py*
script, which takes the name of the data file as an argument and
writes the formatted version to standard out.

The annotation software is written in Java. Although we are providing
the code, it's honestly pretty terrible-- editing it may be more
trouble than it's worth.

Running the code is easy:

::

		java ChatView [filename]

The intro.txt file in the same directory contains a quick tutorial on
using the annotator, which we gave to all our experimental
subjects. Load it into the viewer and follow the instructions.


Scoring and Analysis
--------------------

The main routines for analysis of a single annotation are in
*analysis/chatStats.py*. You can also run this file as a program,
using an annotated file as an argument, to get a variety of
information about the annotation. It will print out some statistics
related to the annotation, then run some baselines and print
statistics about them.

The output looks like this:

::

	Annotation:
	The annotated part of this transcript has 500 lines.
	Non-system lines: 359 .
	36 unique threads.
	The average conversation length is 9.97222222222 .
	The median conversation length is 3 .
	The entropy is 4.0024467585 bits.
	The median chat has 1.0 interruptions per line.
	The average block of 10 contains 2.94555873926 threads.
	The line-averaged conversation density is  2.28969359331 .

At the bottom it prints agreement metrics between the baselines and
the annotation.

::

	Evaluating all1 against human VI: 4.0024467585 MI:
	-8.881784197e-16 1-1-g: 0.197771587744 1-1-o: 0.197771587744 m-1:
	0.197771587744 loc-1: 0.555865921788 loc-2: 0.551820728291 loc-3:
	0.544943820225

VI is variation of information [Meila99]_. MI is mutual
information. 1-1-g is one-to-one overlap, computed by a greedy
algorithm, 1-1-o is one-to-one overlap computed optimally (with the
Hungarian algorithm). m-1 is many-to-one (not by entropy as in the
paper, just treats the human annotation as target), and the loc-N are
local error, as in the paper.

There are a few small scripts that get other information:
*describe.py* gets min/max/mean for some statistics over a collection
of annotations. *printDeltaT.py* prints all the time gaps (sorted) and
*printTimes.py* prints total duration of a
transcript. *speakerStats.py* prints some information on how many
conversations speakers participate in, then scatter-plots
conversations participated in versus utterances spoken.

It's fairly easy to write scripts like this, and the code shouldn't be
too awful.

The *distMat.py* script is the main tool for comparison of different
annotations. To use this tool, you must supply the *--metric* flag,
followed by "121", "m21", "loc3" or "vi", as the first argument. (M21
here does determine source/target by entropy.) Then you must supply a
".annot" file as the second argument. After this, you can supply any
number of ".annot" files, plus "speaker", "alldiff", "all1", "b[#N]"
(blocks of N) or "s[#N]" (pause of N) for baseline annotations of the
dataset.

::

			 % python analysis/distMat.py --metric loc3 IRC/pilot/*.annot speaker

The output is a symmetric matrix of the metric values. min/max/average
or other statistics can be extracted with matlab or some other tool,
and you can also use it for plotting, MDS and so forth.

Finally, you can search for optimal values for block and pause
baselines using *bestBaseline.py*. Here you must supply *--metric*,
*--score*, which must be "max", "min" or "avg", and *--annotator*,
which must be "blocks" or "pause", followed by a list of *.annot*
files.


Training and Testing
--------------------

To test the model, you will first need the unigram statistics and
technical word list. We have included ours (*data/linux-unigrams.dump*
and *data/techwords.dump*) so you don't have to make them. If you
would like to do so anyway, you can make the unigram stats file by
running *unigramStats.py*:

::

	  % python model/unigramStats.py [transcript] [output file]

You can make the techwords file by running "cacheLinuxWords.py":

::

	% python model/cacheLinuxWords.py [directory with linux text] [directory with Penn Treebank parses] [output file]

This program reads its non-linux text from Penn Treebank parse files,
and requires the "InputTree" python interface to the Charniak parser's
tree-reader, which can be obtained from cs.brown.edu/~dmcc. However,
it should be trivial to change this if you want.

Now you can run the test. This takes place in two stages: to do
feature extraction, train the classifier and run it, use
*classifierTest.py*:

::

	% python model/classifierTest.py [training file] [test file] [unigram stats] [tech words list] [working dir]

For instance you can use:

::

	% python model/classifierTest.py IRC/dev/linux-dev-0X.annot IRC/pilot/linux-pilot-0X.annot data/linux-unigrams.dump data/techwords.dump scratch

Currently you can only train or test on one annotation at a
time. (There is no automatic way to find the average classification
error over multiple annotations either-- sorry!) 

The program will create a directory *scratch/129* (129 is the maximum
number of seconds between utterances which the classifier will try to
link.). In this directory are files *keys*, *feats*, *model* and
*predictions*. *keys* contains the indices *i j* of the two utterances
corresponding to each classification instance. For the other file
formats, see the documentation for [megam]_.

To evaluate the classifier, use *model/classifierPrecRec.py [model
dir]* (model dir is a directory created in the previous step, eg
*scratch/129*). This prints precision, recall and balanced F-score of
the *same conversation* class.

Finally, a new annotation can be created using the greedy cut
procedure described in the paper. To do this, use *model/greedy.py*:

::

		  % python model/greedy.py [transcript] [predictions] [keys]

The new transcript (along with some other information which you will
probably need to remove by hand) is printed to standard out. To
evaluate this transcript, see the previous section.

We have included the system annotation of the test set, as
*model/system.annot*. Since the algorithm is deterministic, you should
be able to reproduce this transcript using the instructions here.

References
----------

.. [ElsnerCharniak08] Micha Elsner and Eugene Charniak. "You Talking To Me? A Corpus and Algorithm for Conversation Disentanglement". ACL '08.

.. [Meila99] Marina Meila. "Comparing Clusterings". UW Statistics Technical Reports, COLT '03. http://www.stat.washington.edu/mmp/www.stat.washington.edu/mmp/Papers/compare-colt.pdf

.. [megam] Hal Daume III. Paper at http://pub.hal3.name#daume04cfg-bfgs.pdf, program at http://hal3.name/megam

.. [matplotlib] http://matplotlib.sourceforge.net/

