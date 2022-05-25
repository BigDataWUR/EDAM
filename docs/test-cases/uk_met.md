# UK Meteorological Office

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

## Parse all UK Met weather stations

Following command downloads and stores data from 27 weather stations. 
It is executed in approximately 9 seconds.   

`edam --input "http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{_var_}data.txt" --template uk.tmpl --metadata uk.yaml --var "aberporth,armagh, ballypatrick, camborne, cambridge, cardiff, chivenor, cwmystwyth, dunstaffnage, durham, eastbourne, eskdalemuir"`