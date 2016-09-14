# dispatch_scheduler
A dispatch scheduler simulation that can be modified for personal work. Intended for work with MINERVA collaboration.

# INPUT
Details are pending some stick poking and/or talking with origional authors. Provisionally:

Required configuration/input files:
./config/scheduler.ini ./config/simulation.ini ./config/telescope.ini (Examples are included, and assume you are using the MMT on Mount Hopkins, AZ.)
./dailyprob.txt, containing probabilities of good weather for every observing day. Example included.

./secret/eta_list.txt
This is a target list (presumably generated from SIMBAD and/or exoplanets.org data), with some details (name, location, magnitude, MKK spectral type, exposure time in decimal minutes). It is formatted like a SIMBAD list aside from having an additional exposure time column (and should appropriate scripts or queries be made functional a method will be documented).

# OUTPUT
All of the resulting information from a simulation run is recorded in the results
directory. Each simulation creates its own directory, with a title of 
YYYYMMDD.#####, where the YYYYMMDD is the date the simulation was run, and the
\#\#\#\#\# is an index of the simulation in the folder. E.G. for two simulations 
run on 20160101 and one simulation run on 20160102, the directories produced 
would be 20160101.00001, 20160101.00002, and 20160102.00003. 

Each simulation directory contains a summary file titled as YYYYMMDD.#####.txt,
which matches the name of the directory it was created in. This file will 
contain some of the general information about the simulation, like the 
start and end time, the name of the target list(?), and and others. I'm going 
to put the docstring from the weighting funtion in, among other things. Still
in formulation.

Each target that was observed will have a a file titled NAME.txt, which 
includes a single line header of the columns, and each row after being an 
observation recorded. The information for each observation may change, so I 
will not detail it quite yet. Suffice ot say, the header should do a decent 
job for each column. The columns are tab-delimited, so spliting at the 
string '\t' should work. 

There are also some other files, like sunrise.txt, sunset.txt, and, for each 
target, a NAMErise.txt and NAMEset.txt, which are mostly used in the plotting 
function vis.py. 
