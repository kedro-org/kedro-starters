Feature: kedro-starter-pyspark-iris

  Scenario: Run a Kedro project created from kedro-starter-pyspark-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter
    And I have installed the Kedro project's dependencies
    And I have executed the CLI command to list Kedro pipelines
    Then I should get a successful exit code
