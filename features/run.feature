Feature: Run all starters

  Scenario: Run a Kedro project created from astro-airflow-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from pandas-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pandas-iris
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from pyspark
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pyspark
    And I have installed the Kedro project's dependencies
    When I execute the CLI command to list Kedro pipelines
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from pyspark-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pyspark-iris
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from spaceflights
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code
