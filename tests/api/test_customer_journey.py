"""
Customer User Journey Tests

USER STORY: As a pet shop customer
I want to browse available pets, select one, and place an order
So that I can purchase a pet online

ACCEPTANCE CRITERIA:
- Customer can view available pets
- Customer can view specific pet details
- Customer can place an order for a pet
- Customer can track their order status
"""

import pytest
from framework.test_data_factory import TestDataFactory
from framework.assertions import (
    assert_response_status,
    assert_field_value,
    assert_list_not_empty,
    assert_field_exists,
)


@pytest.mark.customer
class TestCustomerJourney:
    """End-to-end customer journey tests"""

    @pytest.mark.smoke
    def test_01_customer_browses_available_pets(self, api_client, logger):
        """
        GIVEN the customer visits the pet store
        WHEN they browse pets with status 'available'
        THEN they should see a list of available pets
        """
        logger.info("Customer browsing available pets")

        # Create a test pet first to ensure data exists
        test_pet = TestDataFactory.create_pet(status="available")
        create_response = api_client.post("/pet", json=test_pet)
        assert_response_status(create_response, 200, "Failed to create test pet")
        created_pet = create_response.json()

        # Browse available pets
        response = api_client.get("/pet/findByStatus", params={"status": "available"})

        assert_response_status(response, 200, "Failed to fetch available pets")
        pets = response.json()
        assert isinstance(pets, list), "Response should be a list of pets"
        assert_list_not_empty(pets, "Should have at least one available pet")

        # Verify our test pet is in the list
        pet_ids = [pet.get("id") for pet in pets]
        assert created_pet["id"] in pet_ids, "Created pet should be in available list"

        logger.info(f"Found {len(pets)} available pets")

    def test_02_customer_views_pet_details(self, api_client, logger):
        """
        GIVEN the customer has found a pet they're interested in
        WHEN they view the pet's detailed information
        THEN they should see complete pet details including name, category, and status
        """
        # Create a pet for this test
        test_pet = TestDataFactory.create_pet(status="available")
        create_response = api_client.post("/pet", json=test_pet)
        assert_response_status(create_response, 200, "Failed to create test pet")
        created_pet = create_response.json()
        pet_id = created_pet["id"]

        logger.info(f"Customer viewing details for pet ID: {pet_id}")

        response = api_client.get(f"/pet/{pet_id}")

        assert_response_status(response, 200, "Failed to fetch pet details")
        pet_details = response.json()

        # Verify all important fields are present
        assert_field_value(pet_details, "id", pet_id, "Pet ID should match")
        assert_field_exists(pet_details, "name", "Pet should have a name")
        assert_field_exists(pet_details, "status", "Pet should have a status")
        assert_field_value(
            pet_details, "status", "available", "Pet should be available"
        )

        logger.info(f"Pet details verified: {pet_details['name']}")

    @pytest.mark.smoke
    def test_03_customer_places_order(self, api_client, logger):
        """
        GIVEN the customer wants to purchase a pet
        WHEN they place an order for the pet
        THEN the order should be created successfully with 'placed' status
        """
        # Create a pet for this test
        test_pet = TestDataFactory.create_pet(status="available")
        create_response = api_client.post("/pet", json=test_pet)
        assert_response_status(create_response, 200, "Failed to create test pet")
        created_pet = create_response.json()
        pet_id = created_pet["id"]

        logger.info(f"Customer placing order for pet ID: {pet_id}")

        order_data = TestDataFactory.create_order(pet_id=pet_id, quantity=1)
        response = api_client.post("/store/order", json=order_data)

        assert_response_status(response, 200, "Failed to place order")
        order = response.json()

        assert_field_value(order, "petId", pet_id, "Order should reference correct pet")
        assert_field_value(order, "status", "placed", "Order status should be 'placed'")
        assert_field_exists(order, "id", "Order should have an ID")

        logger.info(f"Order placed successfully: Order ID {order['id']}")

    def test_04_customer_checks_order_status(self, api_client, logger):
        """
        GIVEN the customer has placed an order
        WHEN they check their order status
        THEN they should see the current order information
        """
        # Create a pet and order for this test
        test_pet = TestDataFactory.create_pet(status="available")
        create_response = api_client.post("/pet", json=test_pet)
        assert_response_status(create_response, 200, "Failed to create test pet")
        pet_id = create_response.json()["id"]

        order_data = TestDataFactory.create_order(pet_id=pet_id, quantity=1)
        order_response = api_client.post("/store/order", json=order_data)
        assert_response_status(order_response, 200, "Failed to place order")
        order_id = order_response.json()["id"]

        logger.info(f"Customer checking status for order ID: {order_id}")

        response = api_client.get(f"/store/order/{order_id}")

        assert_response_status(response, 200, "Failed to fetch order status")
        order_status = response.json()

        assert_field_value(order_status, "id", order_id, "Order ID should match")
        assert_field_exists(order_status, "status", "Order should have a status")
        assert order_status["status"] in [
            "placed",
            "approved",
            "delivered",
        ], "Order status should be valid"

        logger.info(f"Order status confirmed: {order_status['status']}")

    def test_05_verify_store_inventory(self, api_client, logger):
        """
        GIVEN orders have been placed
        WHEN checking store inventory
        THEN inventory counts should reflect order activity
        """
        logger.info("Verifying store inventory")

        response = api_client.get("/store/inventory")

        assert_response_status(response, 200, "Failed to fetch inventory")
        inventory = response.json()

        assert isinstance(inventory, dict), "Inventory should be a dictionary"
        assert len(inventory) > 0, "Inventory should have status counts"

        logger.info(f"Inventory verified: {len(inventory)} status categories")
