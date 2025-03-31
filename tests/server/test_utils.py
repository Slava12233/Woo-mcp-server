"""
בדיקות למודול utils.py
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch

from woocommerce_mcp.utils import (
    WordPressError,
    create_wp_client,
    create_wc_client,
    handle_response_error
)


@pytest.mark.anyio
async def test_create_wp_client():
    """בדיקה שיצירת לקוח WordPress עובדת כראוי."""
    site_url = "https://example.com"
    username = "test_user"
    password = "test_pass"
    
    # מוק לפונקציית AsyncClient.__init__
    with patch("httpx.AsyncClient") as mock_client:
        # מוק ללקוח שיוחזר
        mock_client_instance = AsyncMock()
        mock_client.return_value = mock_client_instance
        
        # קריאה לפונקציה
        client = await create_wp_client(site_url, username, password)
        
        # בדיקה שהלקוח נוצר עם הפרמטרים הנכונים
        mock_client.assert_called_once()
        call_kwargs = mock_client.call_args[1]
        
        assert call_kwargs["base_url"] == "https://example.com/wp-json/wp/v2"
        assert "auth" in call_kwargs
        assert isinstance(call_kwargs["auth"], httpx.BasicAuth)
        assert call_kwargs["headers"] == {"Content-Type": "application/json"}


@pytest.mark.anyio
async def test_create_wp_client_missing_url():
    """בדיקה שיצירת לקוח WordPress מחזירה שגיאה אם חסרה כתובת אתר."""
    with pytest.raises(WordPressError) as exc_info:
        await create_wp_client("", "user", "pass")
    
    assert "WordPress site URL not provided" in str(exc_info.value)


@pytest.mark.anyio
async def test_create_wp_client_missing_credentials():
    """בדיקה שיצירת לקוח WordPress מחזירה שגיאה אם חסרים פרטי התחברות."""
    with pytest.raises(WordPressError) as exc_info:
        await create_wp_client("https://example.com", "", "")
    
    assert "WordPress credentials not provided" in str(exc_info.value)


@pytest.mark.anyio
async def test_create_wc_client():
    """בדיקה שיצירת לקוח WooCommerce עובדת כראוי."""
    site_url = "https://example.com"
    consumer_key = "test_key"
    consumer_secret = "test_secret"
    
    # מוק לפונקציית AsyncClient.__init__
    with patch("httpx.AsyncClient") as mock_client:
        # מוק ללקוח שיוחזר
        mock_client_instance = AsyncMock()
        mock_client.return_value = mock_client_instance
        
        # קריאה לפונקציה
        client = await create_wc_client(site_url, consumer_key, consumer_secret)
        
        # בדיקה שהלקוח נוצר עם הפרמטרים הנכונים
        mock_client.assert_called_once()
        call_kwargs = mock_client.call_args[1]
        
        assert call_kwargs["base_url"] == "https://example.com/wp-json/wc/v3"
        assert call_kwargs["params"] == {"consumer_key": "test_key", "consumer_secret": "test_secret"}
        assert call_kwargs["headers"] == {"Content-Type": "application/json"}


@pytest.mark.anyio
async def test_create_wc_client_missing_url():
    """בדיקה שיצירת לקוח WooCommerce מחזירה שגיאה אם חסרה כתובת אתר."""
    with pytest.raises(WordPressError) as exc_info:
        await create_wc_client("", "key", "secret")
    
    assert "WordPress site URL not provided" in str(exc_info.value)


@pytest.mark.anyio
async def test_create_wc_client_missing_credentials():
    """בדיקה שיצירת לקוח WooCommerce מחזירה שגיאה אם חסרים פרטי התחברות."""
    with pytest.raises(WordPressError) as exc_info:
        await create_wc_client("https://example.com", "", "")
    
    assert "WooCommerce API credentials not provided" in str(exc_info.value)


def test_handle_response_error_success():
    """בדיקה שטיפול בתגובת HTTP מוצלחת לא מזרוק שגיאה."""
    # יצירת תגובת HTTP מדומה
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    
    # לא אמורה להיזרק שגיאה
    handle_response_error(response, "Test error message")


def test_handle_response_error_failure_json():
    """בדיקה שטיפול בתגובת HTTP כושלת עם JSON תקין מזרוק שגיאה מתאימה."""
    # יצירת תגובת HTTP מדומה
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 404
    response.json.return_value = {"message": "Not Found", "code": "woocommerce_rest_product_invalid_id"}
    
    # בדיקה שנזרקת שגיאה מתאימה
    with pytest.raises(WordPressError) as exc_info:
        handle_response_error(response, "Test error message")
    
    # בדיקת פרטי השגיאה
    assert "Not Found" in str(exc_info.value)
    assert exc_info.value.code == "woocommerce_rest_product_invalid_id"


def test_handle_response_error_failure_no_json():
    """בדיקה שטיפול בתגובת HTTP כושלת ללא JSON תקין מזרוק שגיאה כללית."""
    # יצירת תגובת HTTP מדומה
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 500
    response.json.side_effect = ValueError("Invalid JSON")
    
    # בדיקה שנזרקת שגיאה מתאימה
    with pytest.raises(WordPressError) as exc_info:
        handle_response_error(response, "Test error message")
    
    # בדיקת פרטי השגיאה
    assert "Test error message: 500" in str(exc_info.value) 