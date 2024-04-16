Feature: The customer service back-end
    As a Business Owner
    I need a RESTful customer service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | name  | address         | email                | phone number | id   |
        | James | 4 Wallstreet    | james@email.com      | 1234567890   | 001  |
        | Timmy | 1 Apple Park Way| timmy@email.com      | 2345678901   | 002  |
        | Milo  | 1600 Amphitheatre| milo@email.com      | 3456789012   | 003  |
        | Sammy | 350 Fifth Avenue| sammy@email.com      | 4567890123   | 004  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Address" to "123 Happy St"
    And I set the "Email" to "happy@email.com"
    And I set the "Phone Number" to "5678901234"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Address" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Happy" in the "Name" field
    And I should see "123 Happy St" in the "Address" field
    And I should see "happy@email.com" in the "Email" field
    And I should see "5678901234" in the "Phone Number" field

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "James" in the results
    And I should see "Timmy" in the results
    And I should not see "Milo" in the results

Scenario: Search for customer by name
    When I visit the "Home Page"
    And I set the "Name" to "James"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "James" in the results
    And I should not see "Timmy" in the results
    And I should not see "Milo" in the results

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "Name" to "James"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "James" in the "Name" field
    When I change "Name" to "Logan"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Logan" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Logan" in the results
    And I should not see "James" in the results
