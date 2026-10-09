Feature: Booking movie seats
  As a moviegoer
  I want to browse movies and book seats
  So that I have a place to sit when I arrive

  Background:
    Given a movie called "Dune"
    And an available seat "A1"
    And a booked seat "A2"

  Scenario: Browsing the movie list
    When I open the movie list page
    Then I should see "Dune"

  Scenario: Booking an available seat
    Given I am logged in as "fran"
    When I book seat "A1" for "Dune"
    Then I should see "Booked seat A1 for Dune"
    And seat "A1" should be booked
    When I open my booking history
    Then I should see "Dune"
    And I should see "A1"

  Scenario: Booking a seat that is already taken
    Given I am logged in as "fran"
    When I book seat "A2" for "Dune"
    Then I should see "already booked"
    And I should have 0 bookings

  Scenario: Cancelling a booking frees the seat
    Given I am logged in as "fran"
    And I have booked seat "A1" for "Dune"
    When I cancel my booking for seat "A1"
    Then I should see "Booking cancelled"
    And seat "A1" should be available
    And I should have 0 bookings

  Scenario: Visitors must log in before booking
    Given I am not logged in
    When I try to open the booking page for "Dune"
    Then I should be redirected to the login page

  Scenario: Regular users cannot add movies through the API
    Given I am logged in as "fran"
    When I try to create the movie "Heat" through the API
    Then the response status should be 403

  Scenario: Admins can add movies through the API
    Given I am logged in as an admin
    When I try to create the movie "Heat" through the API
    Then the response status should be 201
