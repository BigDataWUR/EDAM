[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# Table of contents

- [Installation](#installation)   
- [Test cases](#test-cases)   
	- [AgMIP and APSIM weather data files](#agmip-and-apsim-weather-data-files)
		- [AgMIP data files](#agmip-data-files)
			- [AgMIP dataset](#agmip-dataset)
			- [AgMIP template](#agmip-template)
			- [AgMIP metadata](#agmip-metadata)
			- [Parse AgMIP](#parse-agmip)
		- [APSIM station](#apsim-station)
			- [APSIM dataset](#apsim-dataset)
			- [APSIM template](#apsim-template)
			- [APSIM metadata](#apsim-metadata)
			- [Parse APSIM](#parse-apsim)
[Template language](#template-language)   
[Proposed workflow](#proposed-workflow)   
   
# Installation

This project runs on **python3**. Thus, python3 should be installed.   

For MacOS users issuing a `brew install python3` should do the trick. 
Above command installs python3 (`/usr/local/bin/python3`) and pip3 (`/usr/local/bin/pip3`).


You can install and run this version. Issue the followings:

`pip3 install edam`

Above commands install `edam` in your system. 
They also create an **.edam** folder in your system's home directory. 
All EDAM related documents are located in this folder. 
User drafted *template* and *metadat* , and *input* files should be put in this folder. 

More information about the proposed workflow can be found [here](#proposed-worflow). 

# Test cases

After parsing datasets using `edam` command, you can issue `viewer` command 
and a webservice starts on you computer. If no changes to `settings.yaml` 
(check [Proposed workflow](#proposed-workflow)) have been made, you can visit 
`http://127.0.0.1:5000` and view the data. 

For more details about the `edam` command usage, issue a `edam --help` in your terminal.  

## **AgMIP and APSIM weather data files**

The Agricultural Model Intercomparison and Improvement Project (AgMIP) brought into the spotlight agricultural modelling data sharing. 
Within AgMIP, various agricultural models (such as the APSIM) were transformed into the AgMIP data scheme. 

AgMIP and APSIM data files use different *timestamp components*. 
The challenge here is to compose these into one universal timestamp. 
APSIM uses *julian dates* and *years*, while AgMIP timestamp is represented through *year*, *month*, *date* components. 

Another challenge was related with metadata encoded in the preamble of APSIM data files. 
Specifically, prior to the timeseries there are station metadata such as station name, location and others. 
The APSIM data files share the same structure, so these preamble-encoded metadata distinguish the different stations. 


### AgMIP data files

#### AgMIP dataset

```csv
@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM
1980001  1980   1   1  15.0  26.0  12.2   0.0   1.4   4.8   8.6    25
1980002  1980   1   2   6.9  21.2   9.5   0.0   1.6   8.1  10.8    42
1980003  1980   1   3  10.7  22.2  14.7   8.0   1.5  11.9  14.0    52
1980004  1980   1   4  15.6  24.0  10.0   0.0   2.9   9.2  11.7    39
1980005  1980   1   5  16.3  23.9  12.0   0.0   2.7   1.7   6.9    23
1980006  1980   1   6  15.0  23.0  11.8   0.0   2.7   2.8   7.5    26
1980007  1980   1   7  16.5  22.2  11.4   0.0   2.5  -0.5   5.9    22
```

#### AgMIP template

```csv
@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM
{%for timestamp, srad, tmax, tmin, rain, wind, dewp, vprs, rhum in chunk%}
1980001  {{timestamp.year}}   {{timestamp.month}}   {{timestamp.day}}  {{srad.value}}  {{tmax.value}}  {{tmin.value}}   {{rain.value}}   {{wind.value}}   {{dewp.value}}   {{vprs.value}}    {{rhum.value}}
{%endfor%}
```

#### AgMIP metadata

```yaml
Station:
    name: Agmip
    mobile: False
    latitude: 23.200
    longitude: 89.330
    license: Attribution
    tags:
        key1: value1
        key2: value2
Observables:
    - observable_id: tmin
      name: Temperature Min
      ontology: http://edam.gr#Temperature
      qualifiers: http://edam.gr#min
    - observable_id: tmax
      name: Temperature Max
      ontology: http://edam.gr#Temperature
      qualifiers: http://edam.gr#max
    - observable_id: rain
      name: Rain
      ontology: http://edam.gr#Rain
    - observable_id: srad
      name: Solar radiation
      ontology: http://edam.gr#SolarRadiation
    - observable_id: wind
      name: Wind
      ontology: http://edam.gr#WindSpeed
    - observable_id: rhum
      name: Humidity
      ontology: http://edam.gr#RelativeHumidity
    - observable_id: vprs
      name: Vprs
      ontology: http://edam.gr#VaporPressure
    - observable_id: dewp
      name: Dewing point
      ontology: http://edam.gr#DewingPoint
Units of Measurement:
    - name: Megajoule per square metre
      symbol: MJ/m^2
      relevant_observables: srad
    - name: Kilopascal
      symbol: kPa
      relevant_observables: vprs
    - name: Percent
      symbol: \%
      relevant_observables: rhum
    - name: Celcius
      symbol: degC
      relevant_observables: tmin, tmax, dewp
    - name: Millimeters
      symbol: mm
      relevant_observables: rain
    - name: kilometers per hour
      symbol: km/hr
      relevant_observables: wind
```

#### Parse AgMIP

Following command is executed in approximately 2 seconds:

`edam --input Agmip.csv --template Agmip.tmpl --metadata Agmip.yaml --drop yes`   


### APSIM station

#### APSIM dataset

```csv
[weather.met.weather]

Latitude   =   36.68
longitude   =   116.98
tav   =   14.6   (oC)   !   annual   average   ambient   temperature
amp   =   28.2   (oC)   !   annual   amplitude   in   mean   monthly   temperature
!!!!   1/01/1961   to   31/12/2005
   day   year   radn   maxt   mint   rain   wind   RH
   273   2002   17.5   27.2   14.6   0   3.5   54
  274   2002   13.6   23.1   14.7   0   5.3   40
  275   2002   15.8   27.1   11.1   0   5.5   29
  276   2002   15.5   25.8   16.5   0   3.8   39
  277   2002   14.9   25.5   14.6   0   2.5   63
  278   2002   15.2   23.1   15.2   0   3   47
  279   2002   13.4   19.9   10.9   0   3   38
  280   2002   15.7   19.3   8.2   0   2.5   47
```

#### APSIM template

```csv
[weather.met.weather]

Latitude   =   {{station.latitude}}
longitude   =   {{station.longitude}}
tav   =   {{station.tags.tav}}
amp   =   {{station.tags.amp}}
!!!!   1/01/1961   to   31/12/2005
   day   year   radn   maxt   mint   rain   wind   RH
{%for timestamp, radn,maxt,mint,rain,wind,RH in chunk%}
{{timestamp.dayofyear}}  {{timestamp.year}}  {{radn.value}}  {{maxt.value}}  {{mint.value}}  {{rain.value}}  {{wind.value}}  {{RH.value}}
{%endfor%}
```

#### APSIM metadata

```yaml
Station:
    name: Yucheng
    license: Attribution
Observables:
    - observable_id: mint
      name: Temperature
      ontology: http://edam.gr#Temperature
      qualifiers: http://edam.gr#min
    - observable_id: maxt
      name: Max Temperature
      ontology: http://edam.gr#Temperature
      qualifiers: http://edam.gr#max
    - observable_id: rain
      name: Rain
      ontology: http://edam.gr#Rain
    - observable_id: radn
      name: Solar radiation
      ontology: http://edam.gr#SolarRadiation
    - observable_id: wind
      name: Wind
      ontology: http://edam.gr#WindSpeed
    - observable_id: RH
      name: Relative humidity
      ontology: http://edam.gr#RelativeHumidity
Units of Measurement:
    - name: Millijoule per square meters
      symbol: mJ/m^2
      relevant_observables: radn
    - name: Percent
      symbol: \%
      relevant_observables: RH
    - name: Celcius
      symbol: degC
      relevant_observables: mint, maxt
    - name: Millimeters
      symbol: mm
      relevant_observables: rain
    - name: Meters per second
      symbol: m/s
      relevant_observables: wind
```

#### Parse APSIM

Following command is executed in less than 1 second:

`edam --input Yucheng.met --template Yucheng.tmpl --metadata Yucheng.yaml --drop yes`   


## **UK Meteorological Office**

In the context of Open Data, the UK Meteorological Office, reports historical observations of 27 weather stations. 
For every station, monthly observations are stored in one text document. 
New observations are appended every month and each weather station can be found on a certain URI. 
URI follows the pattern: 
`http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{station name}data.txt`, where {station name} is replaced with an actual station name. 

Data points reported in Met Office weather stations' documents have special markers. 
The challenge here is concerned with establishing a relation among markers and attributes. 
This relation, expressed using natural language, is defined in each document's preamble. 
For example, "estimated data is marked with a * after the value". 
These types of metadata are essential, so they have to be parsed and stored. 

### UK Met dataset

```csv
Cwmystwyth
Location: 277300E 274900N, Lat 52.358 Lon -3.802, 301 metres amsl
Estimated data is marked with a * after the value.
Missing data (more than 2 days missing in month) is marked by  ---.
Sunshine data taken from an automatic Kipp & Zonen sensor marked with a #, otherwise sunshine data taken from a Campbell Stokes recorder.
   yyyy  mm   tmax    tmin      af    rain     sun
              degC    degC    days      mm   hours
   1959   1    4.5    -1.9      20    ---     57.2
  1959    2    7.3     0.9      15    ---     87.2
  1959    3    8.4     3.1       3    ---     81.6
  1959    4   10.8     3.7       1    ---    107.4
  1959    5   15.8     5.8       1    ---    213.5
  1959    6   16.9     8.2       0    ---    209.4
  1959    7   18.5     9.5       0    ---    167.8
  1959    8   19.0    10.5       0    ---    164.8
  1959    9   18.3     5.9       0    ---    196.5
  1959   10   14.8     7.9       1    ---    101.1
  1959   11    8.8     3.9       3    ---     38.9
  1959   12    7.2     2.5       3    ---     19.2
```

### UK Met template

```csv
{{station.name}}
Location:{{station.location}}, Lat {{station.latitude}} Lon {{station.longitude}}, {{station.tags.altitude}}
Estimated data is marked with a * after the value.
Missing data (more than 2 days missing in month) is marked by  ---.
Sunshine data taken from an automatic Kipp & Zonen sensor marked with a #, otherwise sunshine data taken from a Campbell Stokes recorder.
   yyyy  mm   tmax    tmin      af    rain     sun
              degC    degC    days      mm   hours
{%for timestamp, tmax,tmin,af,rain,sun in chunk%}
{{timestamp.year}}  {{timestamp.month}}  {{tmax.value}}  {{tmin.value}}  {{af.value}}  {{rain.value}}  {{sun.value}}
{%endfor%}
```

### UK Met metadata

```yaml
Station:
    license: Attribution
    region: United Kingdom
    url: http://www.metoffice.gov.uk/
    tags:
        key1:value1
        key2:value2
Observables:
    -   observable_id: tmin
        name: Temperature minimum
        ontology: http://edam.gr#Temperature
        qualifiers: http://edam.gr#min
    -   observable_id: tmax
        name: Temperature Max
        ontology: http://edam.gr#Temperature
        qualifiers: http://edam.gr#max
    -   observable_id: rain
        name: Rain
        ontology: http://edam.gr#Rain
    -   observable_id: af
        name: Days of air frost
        ontology: http://edam.gr#AirFrostDays
    -   observable_id: sun
        name: Sunshine duration
        ontology: http://edam.gr#SunShineDuration
Units of Measurement:
    -   name: Days
        symbol: D
        relevant_observables: af, sun
    -   name: Celcius
        symbol: degC
        relevant_observables: tmin, tmax
    -   name: Millimeters
        symbol: mm
        relevant_observables: rain
```

### Parse all UK Met weather stations

Following command downloads and stores data from 27 weather stations. 
It is executed in approximately 9 seconds.   

`edam --input "http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{{ var }}data.txt" --template uk.tmpl --metadata uk.yaml --var "aberporth,armagh, ballypatrick, camborne, cambridge, cardiff, chivenor, cwmystwyth, dunstaffnage, durham, eastbourne, eskdalemuir" --drop yes`

## **Australian Bureau of Meteorology (Online)**

Bureau of Meteorology (BoM) in Australia offers historical timeseries from a number of weather stations. 
They concern *daily* observations which are published every month in HTML documents. 
These <!-- documents --> share the same structure and semantics, and are available online. 
Users can access the timeseries by crafting URLs which comprise of information about the requested station id, and month/year. 
For example, the URL for the meteorological data about Adelaide station (*5002* station id) for *October 2017* is:   
[http://www.bom.gov.au/climate/dwo/**201710**/text/IDCJDW**5002**.**201710**.csv](http://www.bom.gov.au/climate/dwo/201710/text/IDCJDW5002.201710.csv)

The challenge in curating BoM timeseries was regarded with their structure. 
In most other cases, every data-row corresponds to *one observation* for a *given timestamp*. 
However, each BoM row has *two observations* for the *same* daily-sampled timestamp. 
These two observations are taken during different time of a day. 
This *sampling hour*, which will complement the *daily-sampled timestamp* for the bi-daily observations, is encoded in the dataset's header.

### BoM dataset

```csv
"Daily Weather Observations for Elliston, South Australia for July 2017"
"Prepared at 13:05 GMT on Monday 21 August 2017   IDCJDW5017.201707"
"Copyright 2003 Commonwealth Bureau of Meteorology"
"Observations were drawn from Elliston {station 018069}"

,"Date","Minimum temperature (°C)","Maximum temperature (°C)","Rainfall (mm)","Evaporation (mm)","Sunshine (hours)","Direction of maximum wind gust ","Speed of maximum wind gust (km/h)","Time of maximum wind gust","9am Temperature (°C)","9am relative humidity (%)","9am cloud amount (oktas)","9am wind direction","9am wind speed (km/h)","9am MSL pressure (hPa)","3pm Temperature (°C)","3pm relative humidity (%)","3pm cloud amount (oktas)","3pm wind direction","3pm wind speed (km/h)","3pm MSL pressure (hPa)"
,2017-07-1,6.4,18.4,0,,,,,,10.0,74,0,,,1024.3,,,,,,
,2017-07-2,10.1,16.6,0,,,,,,12.0,64,0,NNW,19,1014.1,,,,,,
,2017-07-3,7.5,17.3,8.8,,,,,,10.0,90,8,NNW,33,1005.9,,,,,,
,2017-07-4,9.8,16.4,14.2,,,,,,13.4,92,8,NNW,15,1014.1,,,,,,
,2017-07-5,10.5,17.5,27.8,,,,,,14.4,83,6,WSW,17,1017.0,,,,,,
,2017-07-6,5.6,16.1,0.2,,,,,,9.7,68,0,NNW,11,1012.8,,,,,,
,2017-07-7,9.1,15.8,9.2,,,,,,12.6,75,6,SW,37,1015.1,,,,,,
,2017-07-8,8.4,15.7,4.6,,,,,,10.8,97,8,WNW,7,1019.7,,,,,,
,2017-07-9,7.6,15.7,5.0,,,,,,10.8,96,6,NNE,2,1023.2,,,,,,
,2017-07-10,6.9,16.8,0.8,,,,,,11.0,97,6,NNE,2,1027.1,,,,,,
,2017-07-11,5.5,18.6,0,,,,,,9.9,82,1,NNE,4,1030.6,,,,,,
,2017-07-12,8.7,21.2,0,,,,,,12.2,51,6,N,22,1024.5,,,,,,
,2017-07-13,10.0,18.7,0,,,,,,11.9,80,8,NNE,2,1018.0,,,,,,
,2017-07-14,10.6,16.8,3.4,,,,,,13.9,78,7,SSW,11,1020.6,,,,,,
,2017-07-15,8.9,16.0,1.4,,,,,,11.0,82,8,NNW,15,1023.8,,,,,,
,2017-07-16,9.1,15.4,0.2,,,,,,11.7,78,8,N,15,1013.2,,,,,,
,2017-07-17,11.0,15.9,9.4,,,,,,14.5,69,4,WSW,33,1011.2,,,,,,
,2017-07-18,11.0,15.8,5.0,,,,,,12.0,87,8,SSW,28,1018.9,,,,,,
,2017-07-19,11.1,15.2,2.6,,,,,,13.5,72,8,SSE,15,1026.8,,,,,,
,2017-07-20,5.1,14.1,0,,,,,,8.2,84,8,ENE,7,1024.5,,,,,,
,2017-07-21,7.3,22.9,0,,,,,,12.5,60,3,NNE,22,1018.2,,,,,,
,2017-07-22,8.9,20.5,0,,,,,,13.0,61,0,NNW,4,1016.6,,,,,,
,2017-07-23,12.9,18.0,0,,,,,,15.5,86,0,NNW,11,1020.2,,,,,,
,2017-07-24,6.1,21.5,0,,,,,,11.9,89,0,NNE,4,1021.3,,,,,,
,2017-07-25,5.4,18.0,0,,,,,,14.4,99,7,NW,11,1020.2,,,,,,
,2017-07-26,8.3,18.9,0.2,,,,,,10.1,97,2, ,Calm,1025.6,,,,,,
,2017-07-27,6.7,18.4,0,,,,,,16.4,61,8,NNW,22,1016.5,,,,,,
,2017-07-28,4.2,25.6,0.6,,,,,,10.6,89,7,NNE,9,1019.8,,,,,,
,2017-07-29,10.1,17.4,0,,,,,,16.8,70,8,WNW,22,1007.0,,,,,,
,2017-07-30,11.3,16.8,3.6,,,,,,13.1,86,2,WSW,11,1015.9,,,,,,
,2017-07-31,10.3,16.9,5.0,,,,,,12.4,82,6,SSW,22,1022.7,,,,,,
```

### BoM template

```csv
"Daily Weather Observations for {{station.name}}, {{station.region}} for July 2017"
"Prepared at 16:06 GMT on Monday  7 August 2017   IDCJDW5002.201701"
"Copyright 2003 Commonwealth Bureau of Meteorology"
"The "official" Adelaide site is now at West Terrace / ngayirdapira."
"The "official" Adelaide weather observations site is now at West Terrace / ngayirdapira {site number 023000}. This Kent Town site is about 2 km east of the city centre."
"Observations were drawn from Adelaide (Kent Town) {station 023090}"

,"Date","Minimum temperature (°C)","Maximum temperature (°C)","Rainfall (mm)","Evaporation (mm)","Sunshine (hours)","Direction of maximum wind gust ","Speed of maximum wind gust (km/h)","Time of maximum wind gust",{% set hour=9 %},{% set hour=9 %},{% set hour=9 %},{% set hour=9 %},{% set hour=9 %},{%set hour=9 %},{% set hour=15 %},{% set hour=15 %},{%set hour=15 %},{% set hour=15 %},{% set hour=15 %},{% set hour=15 %}
{%for temp, wind, timestamp, windm_spd, windm_dir, wind_spd, wind_dir, rain, evap, sun, humidity, cloud, mlsp, tempMIN, tempMAX in chunk%}
,{{timestamp.date()}},{{tempMIN.value}},{{tempMAX.value}},{{rain.value}},{{evap.value}},{{sun.value}},{{windm_dir.value}},{{windm_spd.value}},{{same_timestamp(windm_spd.timestamp.time, windm_dir.timestamp.time)}},{{temp.value}},{{humidity.value}},{{cloud.value}},{{wind_dir.value}},{{wind_spd.value}},{{mlsp.value}},{{temp.value}},{{humidity.value}},{{cloud.value}},{{wind_dir.value}},{{wind_spd.value}},{{mlsp.value}}
{%endfor%}
```

### Bom metadata

```yaml
Station:
  url: http://www.bom.gov.au
  license: Attribution
Observables:
    - observable_id: temp
      name: Temperature above sea level
    - observable_id: tempMIN
      name: Temperature Min
    - observable_id: tempMAX
      name: Temperature Max
    - observable_id: rain
      name: Rain
    - observable_id: evap
      name: Evapotranspiration
    - observable_id: sun
      name: Sunlight
    - observable_id: windm_dir
      name: Wind max direction
    - observable_id: windm_spd
      name: Wind max speed
    - observable_id: wind_dir
      name: Wind direction
    - observable_id: wind_spd
      name: Wind speed
    - observable_id: humidity
      name: Humidity
    - observable_id: cloud
      name: Cloud
    - observable_id: mlsp
      name: Pressure
Units of Measurement:
    - name: Celcius
      symbol: C
      relevant_observables: temp, tempMIN, tempMAX
    - name: Millimeters
      symbol: mm
      relevant_observables: rain, evap
    - name: hours
      symbol: hr
      relevant_observables: sun
    - name: hectoPascal
      symbol: hPa
      relevant_observables: mlsp
    - name: eights
      symbol: 8th
      relevant_observables: cloud
    - name: Percent
      symbol: \%
      relevant_observables: humidity
    - name: Wind speed
      symbol: km/h
      relevant_observables: wind_spd
    - name: Wind direction
      symbol:
      relevant_observables: windm_dir
```

### Parse all BoM stations for July 2017

The following command will generate the URLs for 574 stations, download, and store them. 
Ultimately 478 stations exist.  
This command takes some time to be executed (aprox. 5 minutes). 

`edam --input "http://www.bom.gov.au/climate/dwo/201707/text/IDCJDW{2-8}0{01-82}.201707.csv" --template bom.tmpl --metadata bom.yaml --drop yes`  

# EDAM template language

## Metadata file

In the metadata file you can define *observables*, *station* and *sensors*. 

An *observable* can have the following attributes: 
1. name (e.g. Wind)
2. unit (e.g. direction km/h)
3. observable_id (e.g. wind). This corresponds to the name one can use in the .tmpl

## Template

In a template one can use in a *placeholder (**{{}}**)* only the *template_id*'s, which were defined in the metadata files. 

A *template_id* can have certain attributes. 
These are:
1. value (e.g.`{{wind.value}}`)
2. timestamp. In case the table (csv) has a dedicated column which denotes the timestamp of a **specific observable**, this will be defined as `{{wind.timestamp.time}}` (if it's in the hh:mm format).
3. In case the one column-timestamp refers to more than one observables (e.g. BoM wind_direction_max and wind_speed_max), this should be defined as `{{same_timestamp(windm_spd.timestamp.time, windm_dir.timestamp.time)}}`

In case a column has the timestamp which corresponds to **all observables in each row**, users will use the `{{timestamp.}}`.  

# Proposed workflow

1. Edit `setting.yaml` to correspond to your database system 
1. Draft a metadata file and put it into metadata folder (~/.edam/metadata)
2. Draft a template file (`~/.edam/templates`)
3. Add your input csv file into inputs folder (`~/.edam/inputs`)