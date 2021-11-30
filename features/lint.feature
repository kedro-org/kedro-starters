Feature: Lint all starters

  Scenario: Lint astro-airflow-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    And I have installed the Kedro project's dependencies
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint pandas-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pandas-iris
    And I have installed the Kedro project's dependencies
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint pyspark starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pyspark
    And I have installed the Kedro project's dependencies
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint pyspark-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter pyspark-iris
    And I have installed the Kedro project's dependencies
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint spaceflights starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights
    And I have installed the Kedro project's dependencies
    When I lint the project
    Then I should get a successful exit code
