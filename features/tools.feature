@skip
Feature: New Kedro project with tools

  Scenario: Create a new Kedro project without any tools
    Given I have prepared a config file with tools "none"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "none"
    Given I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Create a new Kedro project with all tools except 'pyspark'
    Given I have prepared a config file with tools "lint, test, log, docs, data"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "lint, test, log, docs, data"
    Given I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Create a new Kedro project with all tools
    Given I have prepared a config file with tools "all"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "all"
    Given I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Create a new Kedro project with only 'pyspark' tool
    Given I have prepared a config file with tools "pyspark"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "pyspark"
    Given I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code
