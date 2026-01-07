Feature: Package and run all starters

  Scenario: Package astro-airflow-iris project and run packaged project
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter astro-airflow-iris
    When I execute the kedro command "package"
    Then I should get a successful exit code
    When I install the project's python package
    And I execute the installed project
    Then I should get a successful exit code

  Scenario: Package spaceflights-pandas project and run packaged project
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pandas
    When I execute the kedro command "package"
    Then I should get a successful exit code
    When I install the project's python package
    And I execute the installed project
    Then I should get a successful exit code

  @pyspark
  Scenario: Package spaceflights-pyspark project and run packaged project
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter spaceflights-pyspark
    When I execute the kedro command "package"
    Then I should get a successful exit code
    When I install the project's python package
    And I have installed local Spark dependencies
    And I execute the installed project
    Then I should get a successful exit code
