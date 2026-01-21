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

  Scenario: Run a Kedro project created from support-agent-langgraph
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter support-agent-langgraph
    And I have installed the Kedro project's dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  @pyspark
  Scenario: Run a Kedro project created from spaceflights-pyspark
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    And I have installed the Kedro project's dependencies
    And I have installed local Spark dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code
