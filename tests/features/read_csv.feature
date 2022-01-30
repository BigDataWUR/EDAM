# Created by Argyris at 04/11/2021
# Feature: Reading data with EDAM
@csv @reader
Feature: Reading CSV formatted files with EDAM
  We'd like to check the happy flow
  when reading CSV files with EDAM command.

  Scenario: Agmip happy flow
    Given EDAM starts with "Agmip.csv","Agmip.yaml" and "Agmip.tmpl"
    When the user attempts to import data
    Then output contains "8" timeseries