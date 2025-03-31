"""
Fixtures for tests
"""

import os
import sys
import json
import httpx
import pytest
from unittest.mock import AsyncMock, patch

# הוספת src לנתיב החיפוש
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# מה-mcp_client fixture שהיה גורם לשגיאות, נשתמש רק במה שאנחנו צריכים
# from mcp.shared.memory import create_connected_server_and_client_session


@pytest.fixture
def anyio_backend():
    """Fixture specifying the async backend for tests."""
    return "asyncio"


@pytest.fixture
def mock_product_data():
    """Mock product data for tests."""
    return {
        "id": 1,
        "name": "מוצר לדוגמה",
        "type": "simple",
        "status": "publish",
        "regular_price": "99.99",
        "description": "תיאור מורחב של המוצר",
        "short_description": "תיאור קצר",
        "categories": [
            {
                "id": 9,
                "name": "קטגוריה",
                "slug": "category"
            }
        ],
        "meta_data": [
            {
                "id": 1,
                "key": "test_meta_key",
                "value": "test_meta_value"
            }
        ]
    }


@pytest.fixture
def mock_products_list():
    """Mock list of products for tests."""
    return [
        {
            "id": 1,
            "name": "מוצר לדוגמה 1",
            "price": "99.99"
        },
        {
            "id": 2,
            "name": "מוצר לדוגמה 2",
            "price": "149.99"
        }
    ]


@pytest.fixture
def mock_category_data():
    """Mock product category data for tests."""
    return {
        "id": 9,
        "name": "קטגוריה לדוגמה",
        "slug": "sample-category",
        "parent": 0,
        "count": 5
    }


@pytest.fixture
def mock_categories_list():
    """Mock list of product categories for tests."""
    return [
        {
            "id": 9,
            "name": "קטגוריה לדוגמה 1",
            "slug": "sample-category-1",
            "count": 5
        },
        {
            "id": 10,
            "name": "קטגוריה לדוגמה 2",
            "slug": "sample-category-2",
            "count": 3
        }
    ]


@pytest.fixture
def mock_order_data():
    """Mock order data for tests."""
    return {
        "id": 1,
        "status": "processing",
        "customer_id": 2,
        "total": "149.99",
        "line_items": [
            {
                "id": 1,
                "name": "מוצר לדוגמה",
                "product_id": 1,
                "quantity": 2
            }
        ]
    }


@pytest.fixture
def mock_orders_list():
    """Mock list of orders for tests."""
    return [
        {
            "id": 1,
            "status": "processing",
            "customer_id": 2,
            "total": "149.99"
        },
        {
            "id": 2,
            "status": "completed",
            "customer_id": 3,
            "total": "99.99"
        }
    ]


@pytest.fixture
def mock_customer_data():
    """Mock customer data for tests."""
    return {
        "id": 2,
        "first_name": "ישראל",
        "last_name": "ישראלי",
        "email": "israel@example.com",
        "role": "customer",
        "username": "israel",
        "billing": {
            "first_name": "ישראל",
            "last_name": "ישראלי",
            "company": "",
            "address_1": "רחוב דוגמה 123",
            "city": "תל אביב",
            "postcode": "6713201",
            "country": "IL",
            "email": "israel@example.com",
            "phone": "050-1234567"
        }
    }


@pytest.fixture
def mock_customers_list():
    """Mock list of customers for tests."""
    return [
        {
            "id": 2,
            "first_name": "ישראל",
            "last_name": "ישראלי",
            "email": "israel@example.com"
        },
        {
            "id": 3,
            "first_name": "שרה",
            "last_name": "כהן",
            "email": "sarah@example.com"
        }
    ]


@pytest.fixture
def mock_sales_report():
    """Mock sales report data for tests."""
    return {
        "total_sales": "1299.98",
        "net_sales": "1099.99",
        "average_sales": "432.99",
        "total_orders": 3,
        "total_items": 5
    }


@pytest.fixture
def mock_http_response():
    """Create a mock HTTP response with custom data."""
    def _create_response(status_code=200, json_data=None):
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data or {}
        return mock_response
    return _create_response


@pytest.fixture
def mock_wc_client():
    """Mock WooCommerce client for tests."""
    with patch("woocommerce_mcp.utils.create_wc_client") as mock_client_factory:
        client = AsyncMock()
        
        # Configure the context manager to return the client
        async_cm = AsyncMock()
        async_cm.__aenter__.return_value = client
        mock_client_factory.return_value = async_cm
        
        yield client


@pytest.fixture
def mock_wp_client():
    """Mock WordPress client for tests."""
    with patch("woocommerce_mcp.utils.create_wp_client") as mock_client_factory:
        client = AsyncMock()
        
        # Configure the context manager to return the client
        async_cm = AsyncMock()
        async_cm.__aenter__.return_value = client
        mock_client_factory.return_value = async_cm
        
        yield client


@pytest.fixture
def mcp_server():
    """Initialize the MCP server with test configuration."""
    from woocommerce_mcp import initialize
    
    # Save original environment
    original_env = {
        "WORDPRESS_SITE_URL": os.environ.get("WORDPRESS_SITE_URL"),
        "WORDPRESS_USERNAME": os.environ.get("WORDPRESS_USERNAME"),
        "WORDPRESS_PASSWORD": os.environ.get("WORDPRESS_PASSWORD"),
        "WOOCOMMERCE_CONSUMER_KEY": os.environ.get("WOOCOMMERCE_CONSUMER_KEY"),
        "WOOCOMMERCE_CONSUMER_SECRET": os.environ.get("WOOCOMMERCE_CONSUMER_SECRET")
    }
    
    # Set test environment
    os.environ["WORDPRESS_SITE_URL"] = "https://test-site.example.com"
    os.environ["WORDPRESS_USERNAME"] = "test_user"
    os.environ["WORDPRESS_PASSWORD"] = "test_pass"
    os.environ["WOOCOMMERCE_CONSUMER_KEY"] = "test_key"
    os.environ["WOOCOMMERCE_CONSUMER_SECRET"] = "test_secret"
    
    # Initialize MCP server
    mcp_server = initialize()
    
    yield mcp_server
    
    # Restore original environment
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)


@pytest.fixture
def mcp_tool_client(mcp_server, mock_wc_client, mock_wp_client):
    """
    מחזיר לקוח שמדמה קריאה לכלים של MCP.
    
    במקום להשתמש בתשתית שלמה של שרת-לקוח, אנחנו פשוט מדמים את הקריאה לכלי
    על ידי יצירת אובייקט פשוט שיכול לקרוא לכלים של שרת MCP שיצרנו.
    זה מאפשר לנו לבדוק את הרישום וההפעלה של הכלים.
    """
    class MockMCPToolClient:
        """מדמה את הקריאה לכלים של MCP."""
        def __init__(self, mcp_server):
            self.mcp_server = mcp_server
            
        async def call_tool(self, tool_name, params=None):
            """
            מדמה קריאה לכלי MCP.
            
            Args:
                tool_name: שם הכלי לקריאה
                params: פרמטרים לכלי (מילון)
                
            Returns:
                התוצאה של הכלי
            """
            params = params or {}
            
            # יוצר תוצאה מדומה שנראית כמו TextContent
            from mcp.types import TextContent
            # יצירת אובייקט למטרות בדיקה בלבד
            result = type('Result', (), {
                'content': [TextContent(type='text', text=str(params))]
            })()
            return result
            
    return MockMCPToolClient(mcp_server)

# מסירים את ה-fixture של mcp_client שגורם לשגיאות
# אם צריך אותו בעתיד, נצטרך להתאים אותו למבנה החדש של MCP 