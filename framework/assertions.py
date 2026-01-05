"""
Custom assertion helpers for API testing.
Provides clear, informative error messages.
"""
from typing import Any, List, Dict
import requests


def assert_response_status(
    response: requests.Response,
    expected_status: int,
    message: str = None
) -> None:
    """
    Assert response status code.
    
    Args:
        response: Response object to check
        expected_status: Expected HTTP status code
        message: Custom error message
        
    Raises:
        AssertionError: If status code doesn't match expected
        
    Example:
        assert_response_status(response, 200, "Pet creation failed")
    """
    msg = message or f"Expected status {expected_status}, got {response.status_code}"
    
    if response.status_code != expected_status:
        error_detail = f"{msg}\nURL: {response.url}\nResponse: {response.text[:500]}"
        raise AssertionError(error_detail)


def assert_field_value(
    data: dict,
    field: str,
    expected_value: Any,
    message: str = None
) -> None:
    """
    Assert field value in response data.
    
    Args:
        data: Response data dictionary
        field: Field name to check
        expected_value: Expected field value
        message: Custom error message
        
    Raises:
        AssertionError: If field doesn't exist or value doesn't match
        
    Example:
        assert_field_value(pet_data, "status", "available", "Pet status mismatch")
    """
    msg = message or f"Field '{field}' mismatch"
    
    if field not in data:
        raise AssertionError(f"{msg}: Field not found in response\nData: {data}")
    
    if data[field] != expected_value:
        raise AssertionError(
            f"{msg}: Expected '{expected_value}', got '{data[field]}'\nFull data: {data}"
        )


def assert_field_exists(
    data: dict,
    field: str,
    message: str = None
) -> None:
    """
    Assert field exists in response data.
    
    Args:
        data: Response data dictionary
        field: Field name to check
        message: Custom error message
        
    Raises:
        AssertionError: If field doesn't exist
        
    Example:
        assert_field_exists(pet_data, "id", "Pet ID missing")
    """
    msg = message or f"Field '{field}' not found"
    
    if field not in data:
        raise AssertionError(f"{msg}\nAvailable fields: {list(data.keys())}\nData: {data}")


def assert_field_type(
    data: dict,
    field: str,
    expected_type: type,
    message: str = None
) -> None:
    """
    Assert field type in response data.
    
    Args:
        data: Response data dictionary
        field: Field name to check
        expected_type: Expected Python type (int, str, list, dict, etc.)
        message: Custom error message
        
    Raises:
        AssertionError: If field type doesn't match
        
    Example:
        assert_field_type(pet_data, "id", int, "Pet ID should be integer")
    """
    assert_field_exists(data, field, message)
    
    msg = message or f"Field '{field}' type mismatch"
    actual_type = type(data[field])
    
    if not isinstance(data[field], expected_type):
        raise AssertionError(
            f"{msg}: Expected {expected_type.__name__}, got {actual_type.__name__}\nValue: {data[field]}"
        )


def assert_list_not_empty(
    data: List,
    message: str = None
) -> None:
    """
    Assert list is not empty.
    
    Args:
        data: List to check
        message: Custom error message
        
    Raises:
        AssertionError: If list is empty
        
    Example:
        assert_list_not_empty(available_pets, "No available pets found")
    """
    msg = message or "List should not be empty"
    
    if not isinstance(data, list):
        raise AssertionError(f"{msg}: Data is not a list, got {type(data).__name__}")
    
    if len(data) == 0:
        raise AssertionError(msg)


def assert_json_response(
    response: requests.Response,
    message: str = None
) -> Dict:
    """
    Assert response contains valid JSON and return parsed data.
    
    Args:
        response: Response object to check
        message: Custom error message
        
    Returns:
        Parsed JSON data
        
    Raises:
        AssertionError: If response is not valid JSON
        
    Example:
        data = assert_json_response(response, "Invalid JSON response")
    """
    msg = message or "Response is not valid JSON"
    
    try:
        return response.json()
    except ValueError as e:
        raise AssertionError(
            f"{msg}\nStatus: {response.status_code}\nResponse text: {response.text[:500]}\nError: {str(e)}"
        )


def assert_response_time(
    response: requests.Response,
    max_time_ms: int,
    message: str = None
) -> None:
    """
    Assert response time is within limit.
    
    Args:
        response: Response object to check
        max_time_ms: Maximum allowed response time in milliseconds
        message: Custom error message
        
    Raises:
        AssertionError: If response time exceeds limit
        
    Example:
        assert_response_time(response, 1000, "Response too slow")
    """
    response_time_ms = response.elapsed.total_seconds() * 1000
    msg = message or f"Response time exceeded {max_time_ms}ms"
    
    if response_time_ms > max_time_ms:
        raise AssertionError(
            f"{msg}\nActual response time: {response_time_ms:.2f}ms\nURL: {response.url}"
        )


def assert_status_in_list(
    response: requests.Response,
    valid_statuses: List[int],
    message: str = None
) -> None:
    """
    Assert response status is in list of valid statuses.
    
    Args:
        response: Response object to check
        valid_statuses: List of valid HTTP status codes
        message: Custom error message
        
    Raises:
        AssertionError: If status not in valid list
        
    Example:
        assert_status_in_list(response, [200, 201], "Invalid status code")
    """
    msg = message or f"Status {response.status_code} not in valid list {valid_statuses}"
    
    if response.status_code not in valid_statuses:
        raise AssertionError(f"{msg}\nResponse: {response.text[:500]}")
