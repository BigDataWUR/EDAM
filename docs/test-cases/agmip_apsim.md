# AgMIP and APSIM weather data files

The Agricultural Model Intercomparison and Improvement Project (AgMIP) 
brought into the spotlight agricultural modelling data sharing. 
Within AgMIP, various agricultural models (such as the APSIM) were transformed 
into the AgMIP data scheme. 

AgMIP and APSIM data files use different *timestamp components*. 
The challenge here is to compose these into one universal timestamp. 
APSIM uses *julian dates* and *years*, while AgMIP timestamp is 
represented through *year*, *month*, *date* components. 

Another challenge was related with metadata encoded in the preamble 
of APSIM data files. 
Specifically, prior to the timeseries there are station metadata 
such as station name, location and others. 
The APSIM data files share the same structure, so these preamble-encoded 
metadata distinguish the different stations. 