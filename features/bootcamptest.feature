Feature: Bootcamp Assignment

   Scenario: Verify jiskefet log entries
        Given I enter the url http://vm4.jiskefet.io into my browser
        Then I see the title AliceO2 Bookkeeping 2020 in the title
        And I see there are 6 log entries by John Doe
    
    Scenario: Verify jiskefet log content
        When I click on the first log entry
        Then I see the first log is written by John Doe
