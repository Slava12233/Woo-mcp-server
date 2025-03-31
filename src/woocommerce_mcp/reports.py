"""
מודול לניהול דוחות ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error

def register_report_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול דוחות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_sales_report(
        period: str = "month",
        date_min: Optional[str] = None,
        date_max: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר דוח מכירות מ-WooCommerce.
        
        Args:
            period: תקופת הדוח (day, week, month, year).
            date_min: תאריך התחלה (YYYY-MM-DD).
            date_max: תאריך סיום (YYYY-MM-DD).
            filters: מסננים נוספים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני דוח המכירות.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        filters = filters or {}
        
        params = {
            "period": period,
            **filters
        }
        
        if date_min:
            params["date_min"] = date_min
            
        if date_max:
            params["date_max"] = date_max
            
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get("/reports/sales", params=params)
            handle_response_error(response, "Failed to get sales report")
            return response.json()
    
    @mcp.tool()
    async def get_products_report(
        period: str = "month",
        date_min: Optional[str] = None,
        date_max: Optional[str] = None,
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר דוח מוצרים מ-WooCommerce.
        
        Args:
            period: תקופת הדוח (day, week, month, year).
            date_min: תאריך התחלה (YYYY-MM-DD).
            date_max: תאריך סיום (YYYY-MM-DD).
            per_page: מספר תוצאות בדף.
            page: מספר העמוד.
            filters: מסננים נוספים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: נתוני דוח המוצרים.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        filters = filters or {}
        
        params = {
            "period": period,
            "per_page": per_page,
            "page": page,
            **filters
        }
        
        if date_min:
            params["date_min"] = date_min
            
        if date_max:
            params["date_max"] = date_max
            
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get("/reports/products", params=params)
            handle_response_error(response, "Failed to get products report")
            return response.json()
    
    @mcp.tool()
    async def get_customers_report(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר דוח לקוחות מ-WooCommerce.
        
        Args:
            per_page: מספר תוצאות בדף.
            page: מספר העמוד.
            filters: מסננים נוספים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: נתוני דוח הלקוחות.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        filters = filters or {}
        
        params = {
            "per_page": per_page,
            "page": page,
            **filters
        }
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get("/reports/customers", params=params)
            handle_response_error(response, "Failed to get customers report")
            return response.json()
    
    @mcp.tool()
    async def get_stock_report(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר דוח מלאי מ-WooCommerce.
        
        Args:
            per_page: מספר תוצאות בדף.
            page: מספר העמוד.
            filters: מסננים נוספים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: נתוני דוח המלאי.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        filters = filters or {}
        
        params = {
            "per_page": per_page,
            "page": page,
            **filters
        }
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get("/reports/stock", params=params)
            handle_response_error(response, "Failed to get stock report")
            return response.json() 