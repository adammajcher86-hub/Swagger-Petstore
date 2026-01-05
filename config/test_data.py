"""
Static test data and constants.
For dynamic test data, use TestDataFactory in framework package.
"""

# Pet statuses
PET_STATUS = {
    "AVAILABLE": "available",
    "PENDING": "pending",
    "SOLD": "sold"
}

# Order statuses
ORDER_STATUS = {
    "PLACED": "placed",
    "APPROVED": "approved",
    "DELIVERED": "delivered"
}

# Pet categories
PET_CATEGORIES = [
    "Dogs",
    "Cats",
    "Birds",
    "Fish",
    "Reptiles",
    "Small Pets"
]

# API endpoints
ENDPOINTS = {
    "PET": "/pet",
    "PET_BY_ID": "/pet/{petId}",
    "PET_BY_STATUS": "/pet/findByStatus",
    "ORDER": "/store/order",
    "ORDER_BY_ID": "/store/order/{orderId}",
    "INVENTORY": "/store/inventory",
    "USER": "/user",
    "USER_BY_NAME": "/user/{username}"
}

# HTTP status codes
STATUS_CODES = {
    "OK": 200,
    "CREATED": 201,
    "NO_CONTENT": 204,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "INTERNAL_SERVER_ERROR": 500
}

# Test data constraints
CONSTRAINTS = {
    "MAX_PET_NAME_LENGTH": 50,
    "MAX_ORDER_QUANTITY": 100,
    "MIN_PET_ID": 1,
    "MAX_PET_ID": 999999
}
