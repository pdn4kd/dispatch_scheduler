# dispatch_scheduler
A dispatch scheduler simulation that can be modified for personal work. Intended for work with MINERVA collaboration. Run 'simulation.py' to start, or 'vis.py' to visualize the results of previous runs. These scripts should be compatible both Python 2 and 3. Required libraries: collections, configobj, copy, datetime, ephem, glob, math, matplotlib, numpy, os, random, subprocess, sys, time.

For debugging, ipdb may also be needed.


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
contains some of the general information about the simulation. Currently this consists of:
start and end time (in UTC), site name, and instrument name.
Weighting function used is not listed, though probably should be.

Each target that was observed will have a a file titled NAME.txt, which 
includes a single line header of the columns, and each row after being a successful observation. The first observation line is just an initialization, and should not be considered. (An observable object with 0 successful observations will have 2 lines in its output file)
Objects that are not observable (due to telescope limits, dec, RA vs time of year, etc) will not get rise/set files.
The information for each observation may change. Presently shown are:
* Observation start time (JD, easily changeable to other times)
* Observation end time (JD, easily changeable to other times)
* Duration of open shutter observation (decimal minutes). This can be shorter than start time minus end time.
* Altitude (degrees)
* Azimuth (degrees)
* Number of exposures to get the total observation duration
* Observation quality (1 if good, 0 if bad. But bad nights aren't logged...)

All output is in CSV format, despite the .txt name.

There are also some other files, like sunrise.txt, sunset.txt, and for each 
target, a NAMErise.txt and NAMEset.txt, which are mostly used in the plotting 
function vis.py. NAMErise/set files give the rise/set times for that object for the entire simulation period.

i.e.:If the period was 1079 days, and only 475 were suitable for observation, NAMErise.txt will have 1079 lines of data, while NAME.txt will have only 476 (475 observations, plus an initial seeding one that does not correspond to a real observation)

# THINGS TO MODIFY
By default, this code uses varying random seeds. For debugging, you may want to set it to always use the same seed.

Target weighting algorithms are in scheduler.py (a combination of time since last observation and hour angle are used by default, with the base value for time being 2 hours)

You do not have to have all target stars used in a given simulation. In simulation.py, "sim.scheduler.target_list=sim.scheduler.target_list[:500]" selects the first 500. Adjust up/down as desired. You can also sort the list by some feature, such as shortest exposure times. (By default it is shuffled first)
