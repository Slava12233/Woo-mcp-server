"""
מודול לניהול שיטות משלוח ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_shipping_method_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול שיטות משלוח.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_shipping_methods(
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת שיטות משלוח זמינות מ-WooCommerce.
        
        הערה: אלה הן שיטות משלוח שהופעלו בחנות, לא השיטות המופעלות באזורי משלוח ספציפיים.
        
        Args:
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת שיטות המשלוח הזמינות.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get("/shipping_methods")
            
            handle_response_error(response, "Failed to get shipping methods")
            return response.json()

    @mcp.tool()
    async def get_shipping_zone_methods(
        zone_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת שיטות משלוח עבור אזור משלוח ספציפי.
        
        Args:
            zone_id: מזהה אזור המשלוח.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת שיטות המשלוח באזור.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.get(f"/shipping/zones/{zone_id}/methods")
            
            handle_response_error(response, f"Failed to get shipping methods for zone {zone_id}")
            return response.json()

    @mcp.tool()
    async def create_shipping_zone_method(
        zone_id: int,
        method_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר שיטת משלוח חדשה באזור משלוח ב-WooCommerce.
        
        Args:
            zone_id: מזהה אזור המשלוח.
            method_data: נתוני שיטת המשלוח (סוג, כותרת, הגדרות וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני שיטת המשלוח שנוצרה.
        
        Examples:
            >>> method_data = {
            ...     "method_id": "flat_rate",
            ...     "settings": {
            ...         "title": "משלוח רגיל",
            ...         "cost": "10.00"
            ...     }
            ... }
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        if "method_id" not in method_data:
            raise ValueError("method_id is required in method_data")
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.post(
                f"/shipping/zones/{zone_id}/methods",
                json=method_data
            )
            
            handle_response_error(response, f"Failed to create shipping method for zone {zone_id}")
            return response.json()

    @mcp.tool()
    async def update_shipping_zone_method(
        zone_id: int,
        instance_id: int,
        method_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן שיטת משלוח קיימת באזור משלוח ב-WooCommerce.
        
        Args:
            zone_id: מזהה אזור המשלוח.
            instance_id: מזהה שיטת המשלוח (instance_id).
            method_data: נתוני שיטת המשלוח לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני שיטת המשלוח המעודכנת.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.put(
                f"/shipping/zones/{zone_id}/methods/{instance_id}",
                json=method_data
            )
            
            handle_response_error(response, f"Failed to update shipping method {instance_id} for zone {zone_id}")
            return response.json()

    @mcp.tool()
    async def delete_shipping_zone_method(
        zone_id: int,
        instance_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק שיטת משלוח מאזור משלוח ב-WooCommerce.
        
        Args:
            zone_id: מזהה אזור המשלוח.
            instance_id: מזהה שיטת המשלוח (instance_id).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: תוצאת המחיקה.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.delete(f"/shipping/zones/{zone_id}/methods/{instance_id}")
            
            handle_response_error(response, f"Failed to delete shipping method {instance_id} for zone {zone_id}")
            return response.json() 