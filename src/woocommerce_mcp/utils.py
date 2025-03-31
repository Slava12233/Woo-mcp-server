"""
פונקציות עזר ושירות למודולים השונים של שרת ה-MCP של WooCommerce.
"""

import os
from typing import Optional, Dict, Any

import httpx

class WordPressError(Exception):
    """שגיאה שמוחזרת מ-WordPress API."""
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)

async def create_wp_client(
    site_url: str,
    username: str,
    password: str
) -> httpx.AsyncClient:
    """
    יצירת לקוח HTTP עבור WordPress API.
    
    Args:
        site_url: כתובת האתר.
        username: שם משתמש ל-WordPress.
        password: סיסמה ל-WordPress.
    
    Returns:
        httpx.AsyncClient: לקוח HTTP מוגדר.
    
    Raises:
        WordPressError: אם חסרים פרטי התחברות.
    """
    if not site_url:
        raise WordPressError("WordPress site URL not provided")
    
    if not username or not password:
        raise WordPressError("WordPress credentials not provided")
    
    auth = httpx.BasicAuth(username, password)
    return httpx.AsyncClient(
        base_url=f"{site_url}/wp-json/wp/v2",
        auth=auth,
        headers={"Content-Type": "application/json"}
    )

async def create_wc_client(
    site_url: str,
    consumer_key: str,
    consumer_secret: str
) -> httpx.AsyncClient:
    """
    יצירת לקוח HTTP עבור WooCommerce API.
    
    Args:
        site_url: כתובת האתר.
        consumer_key: מפתח צרכן של WooCommerce API.
        consumer_secret: מפתח סודי של WooCommerce API.
    
    Returns:
        httpx.AsyncClient: לקוח HTTP מוגדר.
    
    Raises:
        WordPressError: אם חסרים פרטי התחברות.
    """
    if not site_url:
        raise WordPressError("WordPress site URL not provided")
    
    if not consumer_key or not consumer_secret:
        raise WordPressError("WooCommerce API credentials not provided")
    
    return httpx.AsyncClient(
        base_url=f"{site_url}/wp-json/wc/v3",
        params={"consumer_key": consumer_key, "consumer_secret": consumer_secret},
        headers={"Content-Type": "application/json"}
    )

def handle_response_error(response: httpx.Response, default_message: str) -> None:
    """
    מטפל בשגיאות תגובה מה-API.
    
    Args:
        response: תגובת HTTP.
        default_message: הודעת שגיאה ברירת מחדל.
    
    Raises:
        WordPressError: אם התגובה מכילה שגיאה.
    """
    if response.status_code >= 400:
        try:
            error_data = response.json()
            raise WordPressError(
                error_data.get("message", default_message),
                error_data.get("code")
            )
        except (ValueError, KeyError):
            raise WordPressError(f"{default_message}: {response.status_code}") 