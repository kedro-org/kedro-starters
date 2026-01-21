Feature: Lint all starters

  Scenario: Lint astro-airflow-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint databricks-iris starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter databricks-iris
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint spaceflights-pandas starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint spaceflights-pyspark starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    When I lint the project
    Then I should get a successful exit code

  Scenario: Lint support-agent-langgraph starter
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter support-agent-langgraph
    When I lint the project
    Then I should get a successful exit code