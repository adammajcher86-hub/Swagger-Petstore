"""
Test data factory for generating dynamic, realistic test data.
Uses Faker library to create unique data for each test run.
"""
from faker import Faker
from typing import Dict, Any, List
import random
from config.test_data import PET_STATUS, ORDER_STATUS, PET_CATEGORIES

fake = Faker()


class TestDataFactory:
    """
    Factory class for generating test data.
    
    Ensures unique data for each test run to avoid conflicts.
    Uses Faker for realistic data generation.
    
    Usage:
        pet = TestDataFactory.create_pet(status="available")
        order = TestDataFactory.create_order(pet_id=12345)
    """
    
    @staticmethod
    def create_pet(
        status: str = "available",
        pet_id: int = None,
        name: str = None
    ) -> Dict[str, Any]:
        """
        Generate pet data.
        
        Args:
            status: Pet status (available/pending/sold)
            pet_id: Optional pet ID (generated if not provided)
            name: Optional pet name (generated if not provided)
            
        Returns:
            Dictionary with pet data
            
        Example:
            pet = create_pet(status="available")
        """
        return {
            "id": pet_id or random.randint(100000, 999999),
            "name": name or fake.first_name(),
            "category": {
                "id": random.randint(1, 10),
                "name": random.choice(PET_CATEGORIES)
            },
            "photoUrls": [fake.image_url()],
            "tags": [
                {
                    "id": random.randint(1, 100),
                    "name": fake.word()
                }
            ],
            "status": status
        }
    
    @staticmethod
    def create_order(
        pet_id: int,
        quantity: int = 1,
        order_id: int = None,
        status: str = "placed"
    ) -> Dict[str, Any]:
        """
        Generate order data.
        
        Args:
            pet_id: ID of pet being ordered
            quantity: Number of pets (default: 1)
            order_id: Optional order ID (generated if not provided)
            status: Order status (placed/approved/delivered)
            
        Returns:
            Dictionary with order data
            
        Example:
            order = create_order(pet_id=12345, quantity=1)
        """
        return {
            "id": order_id or random.randint(1, 10000),
            "petId": pet_id,
            "quantity": quantity,
            "shipDate": fake.future_datetime().isoformat() + "Z",
            "status": status,
            "complete": False
        }
    
    @staticmethod
    def create_user(
        username: str = None,
        user_id: int = None
    ) -> Dict[str, Any]:
        """
        Generate user data.
        
        Args:
            username: Optional username (generated if not provided)
            user_id: Optional user ID (generated if not provided)
            
        Returns:
            Dictionary with user data
            
        Example:
            user = create_user()
        """
        return {
            "id": user_id or random.randint(100000, 999999),
            "username": username or fake.user_name(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(length=12),
            "phone": fake.phone_number(),
            "userStatus": 1
        }
    
    @staticmethod
    def create_multiple_pets(
        count: int,
        status: str = "available"
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple pet records.
        
        Args:
            count: Number of pets to generate
            status: Status for all pets
            
        Returns:
            List of pet dictionaries
            
        Example:
            pets = create_multiple_pets(5, status="available")
        """
        return [TestDataFactory.create_pet(status=status) for _ in range(count)]
    
    @staticmethod
    def generate_random_pet_id() -> int:
        """Generate random pet ID"""
        return random.randint(100000, 999999)
    
    @staticmethod
    def generate_random_order_id() -> int:
        """Generate random order ID"""
        return random.randint(1, 10000)
    
    @staticmethod
    def generate_pet_name() -> str:
        """Generate realistic pet name"""
        return fake.first_name()
    
    @staticmethod
    def generate_random_quantity() -> int:
        """Generate random order quantity (1-10)"""
        return random.randint(1, 10)
