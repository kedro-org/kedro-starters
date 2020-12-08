Feature: kedro-starter-pandas-iris

  Scenario: Run a Kedro project created from kedro-starter-pandas-iris
    Given I have prepared a config file
    And I have run a non-interactive kedro new with the starter
    And I have installed the Kedro project's dependencies
    And I have run the Kedro pipeline
    Then I should get a successful exit code
