Feature: Run pytest for all starters

  Scenario: Run pytest for astro-airflow-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    And I have installed the Kedro project's dependencies
    And I have installed pytest
    When I run pytest in the project
    Then I should get a successful exit code

   Scenario: Run pytest for spaceflights-pandas starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas
    And I have installed the Kedro project's dependencies
    And I have installed pytest
    When I run pytest in the project
    Then I should get a successful exit code

  @pyspark
  Scenario: Run pytest for spaceflights-pyspark starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    And I have installed the Kedro project's dependencies
    And I have installed pytest
    When I run pytest in the project
    Then I should get a successful exit code
