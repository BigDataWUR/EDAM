[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# Table of contents

- [Installation](#installation)   
- [Test cases](#test-cases)   
	- [AgMIP and APSIM weather data files](#agmip-and-apsim-weather-data-files)
		- [AgMIP data files](#agmip-data-files)
			- [AgMIP template](#agmip-template)
			- [AgMIP configuration](#agmip-configuration)
			- [Parse AgMIP](#parse-agmip)
		- [APSIM station](#apsim-station)
			- [APSIM template](#apsim-template)
			- [APSIM configuration](#apsim-configuration)
			- [Parse APSIM](#parse-apsim)
[Template language](#template-language)   
[Proposed workflow](#proposed-workflow)   
   
# Installation

This project runs on **python3**. Thus, python3 should be installed.   

For MacOS users issuing a `brew install python3` should do the trick. 
Above command installs python3 (`/usr/local/bin/python3`) and pip3 (`/usr/local/bin/pip3`).

`pip3 install edam`

Above command install `edam` in your system. 
They also create an **.edam** folder in your system's home directory. 
All EDAM related documents are located in this folder. 
User drafted *template* and *configuration* , and *input* files should be put in this folder. 

More information about the proposed workflow can be found [here](#proposed-worflow). 

# Proposed workflow

1. Edit `setting.yaml` to correspond to your database system 
1. Draft a configuration file and put it into configurations folder (~/.edam/configurations)
2. Draft a template file (`~/.edam/templates`)
3. Add your input file into inputs folder (`~/.edam/inputs`)

# Test cases

After parsing datasets using `edam` command, you can issue `viewer` command 
and a webservice starts on you computer. If no changes to `settings.yaml` 
(check [Proposed workflow](#proposed-workflow)) have been made, you can visit 
`http://127.0.0.1:5000` and view the data. 

For more details about the `edam` command usage, issue a `edam --help` in your terminal.  

## **AgMIP and APSIM weather data files**

The Agricultural Model Intercomparison and Improvement Project (AgMIP) brought into the spotlight agricultural modelling data sharing. 
Within AgMIP, various agricultural models (such as the APSIM) were transformed into the AgMIP data scheme. 


### AgMIP data files

#### AgMIP template

```csv
@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM
{%for timestamp, srad, tmax, tmin, rain, wind, dewp, vprs, rhum in chunk%}
1980001  {{timestamp.year}}   {{timestamp.month}}   {{timestamp.day}}  {{srad.value}}  {{tmax.value}}  {{tmin.value}}   {{rain.value}}   {{wind.value}}   {{dewp.value}}   {{vprs.value}}    {{rhum.value}}
{%endfor%}
```

#### AgMIP configuration

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
    1:
        observable_id: tmin
        name: Temperature Min
    2:
        observable_id: tmax
        name: Temperature Max
    3:
        observable_id: rain
        name: Rain
    4:
        observable_id: srad
        name: Solar radiation
    5:
        observable_id: wind
        name: Wind
    39:
        observable_id: rhum
        name: Humidity
    6:
        observable_id: vprs
        name: Vprs
    7:
        observable_id: dewp
        name: Dewing point
        ontology:
Units of Measurement:
    1:
        name: unknown
        symbol:
        ontology:
        relevant_observables: dewp, vprs, srad
    2:
        name: Percent
        symbol: \%
        ontology: something
        relevant_observables: rhum
    3:
        name: Celcius
        symbol: C
        ontology: something
        relevant_observables: tmin, tmax
    4:
        name: Millimeters
        symbol: mm
        ontology: something
        relevant_observables: rain
    5:
        name: kilometers per hour
        symbol: km/h
        ontology: something
        relevant_observables: wind
Sensors:
    1:
        generic: True
        name: Generic Agmip sensor
        manufacturer: Agmip Consortium
        relevant_observables: dewp, vprs, srad, rhum, tmin, tmax, rain, wind
        tags:
            old: True
            analog: False
```

#### Parse AgMIP

Following command is executed in approximately 2 seconds:

`edam --input Agmip.csv --template Agmip.tmpl --config Agmip.yaml --drop yes`   


### APSIM station

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

#### APSIM configuration

```yaml
Station:
    name: Yucheng
    license: Attribution
Observables:
    1:
        observable_id: mint
        name: Temperature minimum
    2:
        observable_id: maxt
        name: Temperature Max
    3:
        observable_id: rain
        name: Rain
    4:
        observable_id: radn
        name: Solar radiation
    5:
        observable_id: wind
        name: Wind
    6:
        observable_id: RH
        name: Relative humidity
Units of Measurement:
    1:
        name: Millijoule per square meters
        symbol: mj/m2
        ontology:
        relevant_observables: radn
    2:
        name: Percent
        symbol: \%
        ontology: something
        relevant_observables: RH
    3:
        name: Celcius
        symbol: C
        ontology: something
        relevant_observables: mint, maxt
    4:
        name: Millimeters
        symbol: mm
        ontology: something
        relevant_observables: rain
    5:
        name: Meters per second
        symbol: m/s
        ontology: something
        relevant_observables: wind
Sensors:
 1:
        generic: True
        name: Generic Agmip sensor
        manufacturer: Agmip Consortium
        relevant_observables: radn, RH, mint, maxt, rain, wind
        tags:
            old: True
            analog: False
```

#### Parse APSIM

Following command is executed in less than 1 second:

`edam --input Yucheng.met --template Yucheng.tmpl --config Yucheng.yaml`   


## **UK Meteorological Office**

In the context of Open Data, the UK Meteorological Office, reports historical observations of 27 weather stations. 
For every station, monthly observations are stored in one text document. 
New observations are appended every month and each weather station can be found on a certain URI. 
URI follows the pattern: 
`http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{station name}data.txt`, where {station name} is replaced with an actual station name. 

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

### UK Met configuration

```yaml
Station:
    license: Attribution
    region: United Kingdom
    url: http://www.metoffice.gov.uk/
Observables:
    1:
        observable_id: tmin
        name: Temperature minimum
    2:
        observable_id: tmax
        name: Temperature Max
    3:
        observable_id: rain
        name: Rain
    4:
        observable_id: af
        name: Days of air frost
    5:
        observable_id: sun
        name: Sunshine duration
Units of Measurement:
    1:
        name: Days
        symbol: D
        ontology:
        relevant_observables: af, sun
    3:
        name: Celcius
        symbol: C
        ontology: something
        relevant_observables: tmin, tmax
    4:
        name: Millimeters
        symbol: mm
        ontology: something
        relevant_observables: rain
Sensors:
 1:
        generic: True
        name: Generic test sensor
        manufacturer: test Consortium
        relevant_observables: tmin, tmax, rain, sun, af
        tags:
            old: True
            analog: False
```

### Parse all UK Met weather stations

Following command downloads and stores data from 27 weather stations. 
It is executed in approximately 9 seconds.   

`edam --input "http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{\$var}data.txt" --template uk.tmpl --config uk.yaml --var "aberporth,armagh, ballypatrick, bradford, braemar, camborne, cambridge, cardiff, chivenor, cwmystwyth, dunstaffnage, durham, eastbourne, eskdalemuir" --drop yes`

## **Australian Bureau of Meteorology (Online)**

Bureau of Meteorology (BoM) in Australia offers historical timeseries from a number of weather stations. 
They concern *daily* observations which are published every month in HTML documents. 
These <!-- documents --> share the same structure and semantics, and are available online. 
Users can access the timeseries by crafting URLs which comprise of information about the requested station id, and month/year. 
For example, the URL for the meteorological data about Adelaide station (*5002* station id) for *October 2017* is:   
[http://www.bom.gov.au/climate/dwo/**201710**/text/IDCJDW**5002**.**201710**.csv](http://www.bom.gov.au/climate/dwo/201710/text/IDCJDW5002.201710.csv)

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

### Bom configuration

```yaml
Station:
  url: http://www.bom.gov.au
  license: Attribution
Observables:
    1:
        observable_id: temp
        name: Temperature above sea level
    15:
        observable_id: tempMIN
        name: Temperature Min
    16:
        observable_id: tempMAX
        name: Temperature Max
    2:
        observable_id: rain
        name: Rain
    3:
        observable_id: evap
        name: Evapotranspiration
    4:
        observable_id: sun
        name: Sunlight
    5:
        observable_id: windm_dir
        name: Wind max direction
    11:
        observable_id: windm_spd
        name: Wind max speed
    6:
        observable_id: wind_dir
        name: Wind direction
    12:
        observable_id: wind_spd
        name: Wind speed
    7:
        observable_id: humidity
        name: Humidity
    8:
        observable_id: cloud
        name: Cloud
    10:
        observable_id: mlsp
        name: Pressure
Units of Measurement:
    1:
        name: Celcius
        symbol: C
        ontology: something
        relevant_observables: temp, tempMIN, tempMAX
    2:
        name: Millimeters
        symbol: mm
        ontology: something
        relevant_observables: rain, evap
    3:
        name: hours
        symbol: hours
        ontology: something
        relevant_observables: sun
    4:
        name: hecto Pascal
        symbol: hPa
        ontology: something
        relevant_observables: mlsp
    5:
        name: eights
        symbol: 8th
        ontology: something
        relevant_observables: cloud
    6:
        name: Percent
        symbol: \%
        ontology: something
        relevant_observables: humidity
    7:
        name: Wind speed
        symbol: km/h
        ontology: something
        relevant_observables: wind_spd, wind_dir
    8:
        name: Wind direction
        symbol:
        ontology: something
        relevant_observables: windm_spd, windm_dir
Sensors:
1:
        generic: True
        name: Generic Bom sensor
        manufacturer: Bom Consortium
        relevant_observables: temp, tempMIN, tempMAX, rain, evap, sun, mlsp, cloud, humidity, windm_spd, windm_dir, wind_spd, wind_dir
        tags:
            old: True
            analog: False

```

### Parse all BoM stations for July 2017

The following command will generate the URLs for 574 stations, download, and store them. 
Ultimately 478 stations exist.  
This command takes some time to be executed (aprox. 5 minutes). 

`edam --input "http://www.bom.gov.au/climate/dwo/201707/text/IDCJDW{2-8}0{01-82}.201707.csv" --template bom.tmpl --config bom.yaml`  

# EDAM template language

## Configuration

In the configuration file you can define *observables*, *station* and *sensors*. 

An *observable* can have the following attributes: 
1. name (e.g. Wind)
2. unit (e.g. direction km/h)
3. observable_id (e.g. wind). This corresponds to the name one can use in the related .tmpl file

## Template

In a template one can use in a *placeholder (**{{}}**)* only the *observable_id*'s, which were defined in the configuration files. 

A *observable_id* has a value attribute (e.g.`{{wind.value}}`)

In case a column has the timestamp which corresponds to **all observables in each row**, users will use the `{{timestamp.}}`.  

