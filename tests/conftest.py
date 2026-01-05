"""
Pytest configuration and shared fixtures.
"""
import pytest
import logging
from framework.api_client import APIClient
from config.environments import Config
import os


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests: dev, qa, staging, prod"
    )


@pytest.fixture(scope="session")
def config(request):
    """
    Get environment configuration for test session.
    
    Usage:
        def test_example(config):
            base_url = config["base_url"]
    """
    env = request.config.getoption("--env")
    os.environ["TEST_ENV"] = env
    return Config.get_config(env)


@pytest.fixture(scope="session")
def api_client(config):
    """
    Create API client for test session.
    
    The client is created once per test session and reused across tests.
    
    Usage:
        def test_example(api_client):
            response = api_client.get("/pet/123")
    """
    client = APIClient(
        base_url=config["base_url"],
        timeout=config["timeout"],
        retry_count=config["retry_count"]
    )
    yield client
    client.close()


@pytest.fixture(scope="function")
def logger():
    """
    Create logger for individual test.
    
    Usage:
        def test_example(logger):
            logger.info("Test started")
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def test_context(request, logger):
    """
    Automatically log test start and end for every test.
    This fixture runs automatically without explicit declaration.
    """
    test_name = request.node.name
    logger.info(f"{'='*80}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'='*80}")
    
    yield
    
    logger.info(f"{'='*80}")
    logger.info(f"Finished test: {test_name}")
    logger.info(f"{'='*80}")


@pytest.fixture(scope="function")
def cleanup_pets(api_client):
    """
    Fixture to track and cleanup created pets after test.
    
    Usage:
        def test_example(api_client, cleanup_pets):
            pet = create_pet()
            cleanup_pets.append(pet["id"])
            # Pet will be deleted after test
    """
    pet_ids = []
    yield pet_ids
    
    # Cleanup after test
    for pet_id in pet_ids:
        try:
            api_client.delete(f"/pet/{pet_id}")
        except Exception as e:
            logging.warning(f"Failed to cleanup pet {pet_id}: {str(e)}")


@pytest.fixture(scope="function")
def cleanup_orders(api_client):
    """
    Fixture to track and cleanup created orders after test.
    
    Usage:
        def test_example(api_client, cleanup_orders):
            order = create_order()
            cleanup_orders.append(order["id"])
            # Order will be deleted after test
    """
    order_ids = []
    yield order_ids
    
    # Cleanup after test
    for order_id in order_ids:
        try:
            api_client.delete(f"/store/order/{order_id}")
        except Exception as e:
            logging.warning(f"Failed to cleanup order {order_id}: {str(e)}")


# Hook to add test information to reports
def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Petstore API Test Report"


def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for critical functionality"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression test suite"
    )
    config.addinivalue_line(
        "markers", "customer: Customer user journey tests"
    )
    config.addinivalue_line(
        "markers", "manager: Store manager user journey tests"
    )
