# Created by argyriossamourkasidis at 04/11/2021
#Feature: Reading data with EDAM
@csv @reader
Feature: Reading CSV formatted files with EDAM
  We'd like to check the happy flow
  when reading CSV files with EDAM command.

  Scenario: Yucheng happy flow
    Given EDAM starts with "Yucheng.met","yucheng.yml" and "yucheng.tmpl"
    When the user attempts to import data
    Then output contains "X" lines