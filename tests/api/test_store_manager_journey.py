"""
Store Manager User Journey Tests

USER STORY: As a pet store manager
I want to manage pet inventory and monitor orders
So that I can maintain accurate stock and fulfill customer orders

ACCEPTANCE CRITERIA:
- Manager can add new pets to inventory
- Manager can update pet information
- Manager can view store inventory status
- Manager can access order information
- Manager can remove sold pets from inventory
"""
import pytest
from framework.test_data_factory import TestDataFactory
from framework.assertions import (
    assert_response_status,
    assert_field_value,
    assert_field_exists
)


@pytest.mark.manager
class TestStoreManagerJourney:
    """End-to-end store manager journey tests"""
    
    @pytest.fixture(scope="class")
    def test_data(self):
        """Shared test data for manager journey"""
        return {
            "pet": None,
            "updated_pet": None,
            "order": None
        }
    
    @pytest.mark.smoke
    def test_01_manager_adds_new_pet_to_inventory(self, api_client, logger, test_data):
        """
        GIVEN the manager receives new pets
        WHEN they add a pet to the system
        THEN the pet should be created with all details and 'available' status
        """
        logger.info("Manager adding new pet to inventory")
        
        pet_data = TestDataFactory.create_pet(status="available")
        response = api_client.post("/pet", json=pet_data)
        
        assert_response_status(response, 200, "Failed to add pet to inventory")
        created_pet = response.json()
        test_data["pet"] = created_pet
        
        assert_field_exists(created_pet, "id", "Created pet should have an ID")
        assert_field_value(created_pet, "name", pet_data["name"], "Pet name should match")
        assert_field_value(created_pet, "status", "available", "New pet should be available")
        
        logger.info(f"Pet added successfully: ID {created_pet['id']}, Name: {created_pet['name']}")
    
    def test_02_manager_updates_pet_information(self, api_client, logger, test_data):
        """
        GIVEN a pet exists in inventory
        WHEN the manager updates the pet's information
        THEN the changes should be saved successfully
        """
        pet = test_data["pet"]
        logger.info(f"Manager updating pet ID: {pet['id']}")
        
        # Update pet details
        updated_data = pet.copy()
        updated_data["name"] = f"{pet['name']}_Updated"
        updated_data["status"] = "pending"
        
        response = api_client.put("/pet", json=updated_data)
        
        assert_response_status(response, 200, "Failed to update pet")
        updated_pet = response.json()
        test_data["updated_pet"] = updated_pet
        
        assert_field_value(updated_pet, "name", updated_data["name"], "Pet name should be updated")
        assert_field_value(updated_pet, "status", "pending", "Pet status should be updated")
        
        logger.info(f"Pet updated: New name '{updated_pet['name']}', Status: {updated_pet['status']}")
    
    def test_03_manager_verifies_update_persisted(self, api_client, logger, test_data):
        """
        GIVEN the manager has updated a pet
        WHEN they retrieve the pet again
        THEN the updates should be persisted
        """
        pet_id = test_data["updated_pet"]["id"]
        logger.info(f"Manager verifying persisted updates for pet ID: {pet_id}")
        
        response = api_client.get(f"/pet/{pet_id}")
        
        assert_response_status(response, 200, "Failed to fetch updated pet")
        pet = response.json()
        
        assert_field_value(pet, "name", test_data["updated_pet"]["name"], "Name update should persist")
        assert_field_value(pet, "status", "pending", "Status update should persist")
        
        logger.info("Updates verified as persisted")
    
    @pytest.mark.smoke
    def test_04_manager_reviews_store_inventory(self, api_client, logger):
        """
        GIVEN the store has various pets with different statuses
        WHEN the manager reviews inventory
        THEN they should see counts for each status category
        """
        logger.info("Manager reviewing store inventory")
        
        response = api_client.get("/store/inventory")
        
        assert_response_status(response, 200, "Failed to fetch inventory")
        inventory = response.json()
        
        assert isinstance(inventory, dict), "Inventory should be a dictionary of statuses"
        # Verify expected status categories exist
        expected_statuses = ["available", "pending", "sold"]
        for status in expected_statuses:
            if status in inventory:
                assert isinstance(inventory[status], int), f"{status} count should be integer"
                logger.info(f"Inventory - {status}: {inventory[status]}")
    
    def test_05_manager_marks_pet_as_sold(self, api_client, logger, test_data):
        """
        GIVEN a pet has been purchased
        WHEN the manager updates the pet status to 'sold'
        THEN the pet should no longer appear as available
        """
        pet = test_data["updated_pet"]
        logger.info(f"Manager marking pet ID {pet['id']} as sold")
        
        sold_data = pet.copy()
        sold_data["status"] = "sold"
        
        response = api_client.put("/pet", json=sold_data)
        
        assert_response_status(response, 200, "Failed to mark pet as sold")
        sold_pet = response.json()
        
        assert_field_value(sold_pet, "status", "sold", "Pet should be marked as sold")
        
        logger.info("Pet successfully marked as sold")
    
    def test_06_manager_verifies_sold_pet_not_available(self, api_client, logger, test_data):
        """
        GIVEN a pet has been marked as sold
        WHEN searching for available pets
        THEN the sold pet should not appear in results
        """
        sold_pet_id = test_data["updated_pet"]["id"]
        logger.info("Manager verifying sold pet not in available list")
        
        response = api_client.get("/pet/findByStatus", params={"status": "available"})
        
        assert_response_status(response, 200, "Failed to fetch available pets")
        available_pets = response.json()
        
        available_pet_ids = [pet["id"] for pet in available_pets]
        assert sold_pet_id not in available_pet_ids, "Sold pet should not be in available list"
        
        logger.info("Verified: Sold pet correctly excluded from available inventory")
    
    def test_07_manager_removes_pet_from_system(self, api_client, logger, test_data):
        """
        GIVEN a pet needs to be removed from the system
        WHEN the manager deletes the pet
        THEN the pet should no longer be retrievable
        """
        pet_id = test_data["updated_pet"]["id"]
        logger.info(f"Manager removing pet ID {pet_id} from system")
        
        # Delete the pet
        delete_response = api_client.delete(f"/pet/{pet_id}")
        assert_response_status(delete_response, 200, "Failed to delete pet")
        
        # Verify pet is gone
        get_response = api_client.get(f"/pet/{pet_id}")
        assert get_response.status_code == 404, "Deleted pet should return 404"
        
        logger.info("Pet successfully removed from system")
