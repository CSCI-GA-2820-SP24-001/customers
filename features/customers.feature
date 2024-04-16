Feature: The customer service back-end
    As a online shop owner
    I need a RESTful catalog service
    So that I can keep track of all my customer

Background:
    Given the following customers
        | name       | address         | email                | phone
        | Albert     | 4000 Penn Ave   | albert@gmail.com     | 212-123-4567
        | Ben        | 44 West 4th St  | ben@outlook.com      | 212-309-3131
        | Carol      | 1 Wall Street   | Carol@stern.nyu.edu  | 601-932-2222
        | Dillan     | 611 5th Ave     | Dillan@nyu.edu       | 714-888-8888

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Pet
    When I visit the "Home Page"
    And I set the "Name" to "Eileen"
    And I set the "Address" to "50 Broadway St"
    And I set the "Email" to "eileen@gmail.com"
    And I set the "phone" to "999-888-7777"
    And I press the "Create" button
    Then I should see the message "Success"