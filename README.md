# <span style="font-family:Papyrus; font-size:35px;"><span style="color: rgb(112,156,96);">**E**</span>nvironmental <span style="color: rgb(140,201,200);">**D**</span>ata <span style="color: rgb(245,74,57);">**A**</span>cquisition <span style="color: rgb(21,97,101);">**M**</span>odule</span>

EDAM (Environmental Data Acquisition Module), is a template framework that facilitates 
timeseries data acquisition and integration. EDAM templates are written using programming 
language-agnostic semantics, and can be reused both for input and output, thus enabling 
data reuse via transformations across different formats.

---
[![Downloads](https://pepy.tech/badge/edam)](https://pepy.tech/project/edam)
[![Documentation Status](https://readthedocs.org/projects/edam/badge/?version=latest)](https://edam.readthedocs.io/en/latest/?badge=latest)
[![Supported Versions](https://img.shields.io/pypi/pyversions/edam.svg)](https://pypi.org/project/edam)

---

# Installation

This project runs on **python3**. Thus, python3 should be installed.

It is highly recommended installing the module via Python virtual environment
You can install and run this version. Issue the followings:

`pip install edam`

Above command installs `edam`, which will be available to the virtual environment. 
It also creates an **.edam** folder in your system's home directory. 
All EDAM related documents are located in this folder. 
User=drafted *template* and *metadata*, and *input* files should be placed 
under these corresponding directories. 

More information about the proposed workflow can be found 
in the [proposed-workflow](#proposed-workflow). 

# Table of contents

- [Installation](#installation)   
- [EDAM template language](#edam-template-language)   
- [Proposed workflow](#proposed-workflow)
- [Test cases](#test-cases)   
  - [AgMIP and APSIM weather data files](#agmip-and-apsim-weather-data-files)
     - [AgMIP data files](#agmip-data-files)
     - [APSIM station](#apsim-station)
  - [UK Meteorological Office](#uk-meteorological-office)


# EDAM template language

## Metadata file

In the metadata file you can define *observables*, *station* and *sensors*. 

An *observable* can have the following attributes: 
1. name (e.g. Wind)
2. unit (e.g. direction km/h)
3. observable_id (e.g. wind). This corresponds to the name one can use in the .tmpl

## Template

In a template one can use in a *placeholder (**{{}}**)* only the 
*template_id*'s, which were defined in the metadata files. 

A *template_id* can have certain attributes. 
These are:
1. value (e.g.`{{wind.value}}`)
2. timestamp. In case the table (csv) has a dedicated column which denotes the timestamp of a **specific observable**, this will be defined as `{{wind.timestamp.time}}` (if it's in the hh:mm format).
3. In case the one column-timestamp refers to more than one observable (e.g. BoM wind_direction_max and wind_speed_max), this should be defined as `{{same_timestamp(windm_spd.timestamp.time, windm_dir.timestamp.time)}}`

In case a column has the timestamp which corresponds to 
**all observables in each row**, users will use the `{{timestamp.}}`.  

# Proposed workflow

1. Edit `setting.yaml` to correspond to your database system 
1. Draft a metadata file and put it into metadata folder (`~/.edam/metadata`)
2. Draft a template file (`~/.edam/templates`)
3. Add your input csv file into inputs folder (`~/.edam/inputs`)

# Test cases

After parsing datasets using `edam` command, you can issue `viewer` command 
and a webservice starts on you computer. If no changes to `settings.yaml` 
(check [Proposed workflow](#proposed-workflow)) have been made, you can visit 
`http://127.0.0.1:5000` and view the data. 

For more details about the `edam` command usage, 
issue a `edam --help` in your terminal.  

## **AgMIP and APSIM weather data files**

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


### AgMIP data files

<details>
    <summary><code>AgMIP dataset</code></summary>

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
</details>

<details>
    <summary><code>AgMIP template</code></summary>

```csv
@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM
{%for timestamp, srad, tmax, tmin, rain, wind, dewp, vprs, rhum in chunk%}
1980001  {{timestamp.year}}   {{timestamp.month}}   {{timestamp.day}}  {{srad.value}}  {{tmax.value}}  {{tmin.value}}   {{rain.value}}   {{wind.value}}   {{dewp.value}}   {{vprs.value}}    {{rhum.value}}
{%endfor%}
```
</details>

<details>
    <summary><code>AgMIP metadata</code></summary>

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
      ontology: https://edam.org#Temperature
      qualifiers: https://edam.org#min
    - observable_id: tmax
      name: Temperature Max
      ontology: https://edam.org#Temperature
      qualifiers: https://edam.org#max
    - observable_id: rain
      name: Rain
      ontology: https://edam.org#Rain
    - observable_id: srad
      name: Solar radiation
      ontology: https://edam.org#SolarRadiation
    - observable_id: wind
      name: Wind
      ontology: https://edam.org#WindSpeed
    - observable_id: rhum
      name: Humidity
      ontology: https://edam.org#RelativeHumidity
    - observable_id: vprs
      name: Vprs
      ontology: https://edam.org#VaporPressure
    - observable_id: dewp
      name: Dewing point
      ontology: https://edam.org#DewingPoint
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
</details>

#### Parse AgMIP

Following command is executed in approximately 2 seconds:

`edam --input Agmip.csv --template Agmip.tmpl --metadata Agmip.yaml`   


### APSIM station

<details>
    <summary><code>APSIM dataset</code></summary>

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
</details>

<details>
    <summary><code>APSIM template</code></summary>

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
</details>

<details>
    <summary><code>APSIM metadata</code></summary>

```yaml
Station:
    name: Yucheng
    license: Attribution
Observables:
    - observable_id: mint
      name: Temperature
      ontology: https://edam.org#Temperature
      qualifiers: https://edam.org#min
    - observable_id: maxt
      name: Max Temperature
      ontology: https://edam.org#Temperature
      qualifiers: https://edam.org#max
    - observable_id: rain
      name: Rain
      ontology: https://edam.org#Rain
    - observable_id: radn
      name: Solar radiation
      ontology: https://edam.org#SolarRadiation
    - observable_id: wind
      name: Wind
      ontology: https://edam.org#WindSpeed
    - observable_id: RH
      name: Relative humidity
      ontology: https://edam.org#RelativeHumidity
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

</details>

#### Parse APSIM

Following command is executed in less than 1 second:

`edam --input Yucheng.met --template Yucheng.tmpl --metadata Yucheng.yaml`   


## **UK Meteorological Office**

In the context of Open Data, the UK Meteorological Office, reports historical 
observations of 27 weather stations. 
For every station, monthly observations are stored in one text document. 
New observations are appended every month and each weather station can be 
found on a certain URI. 
URI follows the pattern: 
`http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{station name}data.txt`, 
where {station name} is replaced with an actual station name. 

Data points reported in Met Office weather stations' documents have 
special markers. 
The challenge here is concerned with establishing a relation 
among markers and attributes. 
This relation, expressed using natural language, is defined 
in each document's preamble. 
For example, "estimated data is marked with a * after the value". 
These types of metadata are essential, so they have to be parsed and stored.

<details>
    <summary><code>UK Met dataset</code></summary>

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

</details>

<details>
    <summary><code>UK Met template</code></summary>

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

</details>

<details>
    <summary><code>UK Met metadata</code></summary>

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
        ontology: https://edam.org#Temperature
        qualifiers: https://edam.org#min
    -   observable_id: tmax
        name: Temperature Max
        ontology: https://edam.org#Temperature
        qualifiers: https://edam.org#max
    -   observable_id: rain
        name: Rain
        ontology: https://edam.org#Rain
    -   observable_id: af
        name: Days of air frost
        ontology: https://edam.org#AirFrostDays
    -   observable_id: sun
        name: Sunshine duration
        ontology: https://edam.org#SunShineDuration
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

</details>

### Parse all UK Met weather stations

Following command downloads and stores data from 27 weather stations. 
It is executed in approximately 9 seconds.   

`edam --input "http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{_var_}data.txt" --template uk.tmpl --metadata uk.yaml --var "aberporth,armagh, ballypatrick, camborne, cambridge, cardiff, chivenor, cwmystwyth, dunstaffnage, durham, eastbourne, eskdalemuir"`