# Template

In a template one can use in a *placeholder (**{{}}**)* only the 
*template_id*'s, which were defined in the metadata files. 

A *template_id* can have certain attributes. 
These are: 

1. value (e.g.`{{wind.value}}`)
2. timestamp. In case the table (csv) has a dedicated column which denotes the timestamp of a **specific observable**, this will be defined as `{{wind.timestamp.time}}` (if it's in the hh:mm format).
3. In case the one column-timestamp refers to more than one observable (e.g. BoM wind_direction_max and wind_speed_max), this should be defined as `{{same_timestamp(windm_spd.timestamp.time, windm_dir.timestamp.time)}}`

In case a column has the timestamp which corresponds to 
**all observables in each row**, users will use the `{{timestamp.}}`.  