# Created by Argyris at 04/11/2021
# Feature: Reading data with EDAM
@csv @reader
Feature: Reading CSV formatted files with EDAM
  We'd like to check the happy flow
  when reading CSV files with EDAM command.

  Scenario Outline: <station> happy flow
    Given EDAM starts with "<station>.csv","<station>.yaml" and "<station>.tmpl"
    When the user attempts to import data
    Then output contains "<number>" timeseries

    Examples:
      | station | number |
      | Agmip   | 8      |
      | Bioma   | 7      |