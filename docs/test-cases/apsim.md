# APSIM station

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

## Parse APSIM

Following command is executed in less than 1 second:

`edam --input Yucheng.met --template Yucheng.tmpl --metadata Yucheng.yaml`   