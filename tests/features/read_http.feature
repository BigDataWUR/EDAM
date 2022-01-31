# Created by Argyris at 31/01/2022
# Feature: Reading data with EDAM via HTTP
@http @reader
Feature: Reading with EDAM from HTTP
  We'd like to check the happy flow
  when reading with EDAM via HTTP command.

  Scenario Outline: <station> happy flow
    Given EDAM starts with "<filename>","<station>.yaml" and "<station>.tmpl"
    When the user attempts to import data
    Then output contains "<number>" timeseries

    Examples:
      | station | filename                                                                               | number |
      | uk      | https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/aberporthdata.txt | 5      |