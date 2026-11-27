Feature: Lint all starters

  Scenario: Lint astro-airflow-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    Then the project should declare its development tools in a dependency group
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint databricks-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter databricks-iris
    Then the project should declare its development tools in a dependency group
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint spaceflights-pandas starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas
    Then the project should declare its development tools in a dependency group
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint spaceflights-pyspark starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    Then the project should declare its development tools in a dependency group
    When I lint the project
    Then I should get a successful exit code
