Feature: New Kedro project with tools

  @pyspark
  Scenario: Create a new Kedro project with all tools
    Given I have prepared a config file with tools "all"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "all"
    Given I have installed the Kedro project's dependencies
    And I have installed local Spark dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code

  @pyspark
  Scenario: Create a new Kedro project with only 'pyspark' tool
    Given I have prepared a config file with tools "pyspark"
    When I run a non-interactive kedro new without starter
    Then the expected tool directories and files should be created with "pyspark"
    Given I have installed the Kedro project's dependencies
    And I have installed local Spark dependencies
    When I run the Kedro pipeline
    Then I should get a successful exit code
