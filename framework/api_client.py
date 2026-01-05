"""
Robust API client with retry logic and comprehensive error handling.
"""
import requests
import logging
from typing import Dict, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class APIClient:
    """
    HTTP client with built-in retry logic and error handling.
    
    Features:
    - Automatic retry on transient failures
    - Request/response logging
    - Session management
    - Configurable timeouts
    
    Usage:
        client = APIClient(base_url="https://api.example.com", timeout=30)
        response = client.get("/endpoint")
    """
    
    def __init__(self, base_url: str, timeout: int = 30, retry_count: int = 3):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API requests
            timeout: Default timeout for requests in seconds
            retry_count: Number of retries for failed requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = self._create_session(retry_count)
        logger.info(f"APIClient initialized with base_url: {self.base_url}")
        
    def _create_session(self, retry_count: int) -> requests.Session:
        """
        Create requests session with retry strategy.
        
        Args:
            retry_count: Number of retries for failed requests
            
        Returns:
            Configured requests Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Generic request method with logging.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (will be appended to base_url)
            **kwargs: Additional arguments passed to requests
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        
        # Log request details
        logger.info(f"{method.upper()} {url}")
        if 'json' in kwargs:
            logger.debug(f"Request body: {kwargs['json']}")
        if 'params' in kwargs:
            logger.debug(f"Query params: {kwargs['params']}")
        
        # Make request
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            
            # Log response
            logger.info(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text[:500]}")  # First 500 chars
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (typically json=data)
            
        Returns:
            Response object
        """
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send PUT request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (typically json=data)
            
        Returns:
            Response object
        """
        return self.request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send DELETE request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self.request("DELETE", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send PATCH request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (typically json=data)
            
        Returns:
            Response object
        """
        return self.request("PATCH", endpoint, **kwargs)
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("APIClient session closed")
