######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Steps

Steps file for products.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    #
    # List all of the products and delete them one by one
    #
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    #
    # load the database with new products
    #
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Cloths" in the "Category" dropdown
    And I should see "59.95" in the "Price" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "A red fedora" in the "Description" field
    When I change "Name" to "Fedora"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Fedora" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Fedora" in the results
    And I should not see "Hat" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "A red fedora" in the "Description" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Hat" in the results

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

Scenario: Search by category
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "Food" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Sheets" in the results

Scenario: Search by available
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

Scenario: Search by name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
