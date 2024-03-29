# Created by Argyris at 04/11/2021
# Feature: Reading data with EDAM
Feature: Reading CSV formatted files with EDAM
  We'd like to check the happy flow
  when reading CSV files with EDAM command.

  Scenario Outline: <station> happy flow
    Given EDAM starts with "<filename>","<station>.yaml" and "<station>.tmpl"
    When the user attempts to import data
    Then output contains "<number>" timeseries

    Examples:
      | station | filename  | number |
      | Agmip   | Agmip.csv | 8      |
      | uk      | uk.txt    | 5      |