# AgMIP data files

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

## Parse AgMIP

Following command is executed in approximately 2 seconds:

`edam --input Agmip.csv --template Agmip.tmpl --metadata Agmip.yaml`  