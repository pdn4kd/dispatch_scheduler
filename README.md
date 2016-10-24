# dispatch_scheduler
A dispatch scheduler simulation that can be modified for personal work. Intended for work with MINERVA collaboration. Run 'simulation.py' to start. These scripts should be compatible both Python 2 and 3. Required libraries: collections, configobj, copy, datetime, ephem, glob, ipdb*, math, matplotlib, numpy, os, random, subprocess, sys, time.

*currently attempting to deprecate.


# INPUT
Details are pending some stick poking and/or talking with original authors. Provisionally:

Required configuration/input files:
./config/scheduler.ini ./config/simulation.ini ./config/telescope.ini (Examples are included, and assume you are using the MINERVA array on Mount Hopkins, AZ. Also included are prefixed versions with more or less accurate data for the WIYN, LBT, and a backup of MINERVA)
./dailyprob.txt, containing probabilities of good weather for every observing day. Example based off of Kitt Peak from 1999-2006 included. This file has a minimum size (364 rows/days).

./secret/eta_list.txt
This is a target list (presumably generated from SIMBAD and/or exoplanets.org data), with some details (name, location, magnitude, MKK spectral type, exposure time in decimal minutes). It is formatted like a SIMBAD list aside from having an additional exposure time column (and should appropriate scripts or queries be made functional a method will be documented). This specific location may be modified in the configuration files if all the hard-coded parts are gone. Allowed RA/Dec can be filtered by editing simbad_reader.py

# OUTPUT
All of the resulting information from a simulation run is recorded in the results
directory. Each simulation creates its own directory, with a title of 
YYYYMMDD.#####, where the YYYYMMDD is the date the simulation was run, and the
\#\#\#\#\# is an index of the simulation in the folder. E.G. for two simulations 
run on 20160101 and one simulation run on 20160102, the directories produced 
would be 20160101.00001, 20160101.00002, and 20160102.00003. 

Each simulation directory contains a summary file titled as YYYYMMDD.#####.txt,
which matches the name of the directory it was created in. This file 
contains some of the general information about the simulation, like the 
start and end time (in UTC), the name of the target list(?), and and others. I'm going 
to put the docstring from the weighting funtion in, among other things. Still
in formulation.

Each target that was observed will have a a file titled NAME.txt, which 
includes a single line header of the columns, and each row after being a successful observation. The first observation line is just an initialization, and should not be considered. (An observable object with 0 successful observations will have 2 lines in its output file)
Objects that are not observable (due to telescope limits, dec, RA vs time of year, etc) will not get rise/set files.
The information for each observation may change. Presently shown are:
* Observation start time (JD, easily changeable to other times)
* Observation end time (JD, easily changeable to other times)
* Duration of observation (decimal seconds)
* Altitude (degrees)
* Azimuth (degrees)
* Observation quality (1 if good, 0 if bad. But bad nights aren't logged...)
The columns are tab-delimited, so spliting at the string '\t' should work. 

There are also some other files, like sunrise.txt, sunset.txt, and for each 
target, a NAMErise.txt and NAMEset.txt, which are mostly used in the plotting 
function vis.py. NAMErise/set files give the rise/set times for that object for the entire simulation period.

i.e.:If the period was 1079 days, and only 475 were suitable for observation, NAMErise.txt will have 1079 lines of data, while NAME.txt will have only 475
