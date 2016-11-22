Feature: Test a login form

Scenario: Test Login
  Given I go to my login form
  Then the title should be "Login Form - CrossBrowserTesting.com"
  When I enter my credentials
  When I click login
  Then I should see the login message
