Feature: Run all starters

  Scenario: Run a Kedro project created from astro-airflow-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from spaceflights-pandas
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from spaceflights-pandas-viz
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas-viz
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from spaceflights-pyspark
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  Scenario: Run a Kedro project created from spaceflights-pyspark-viz
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark-viz
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code
