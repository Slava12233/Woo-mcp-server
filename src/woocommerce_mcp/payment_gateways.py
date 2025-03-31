"""
מודול לניהול שערי תשלום ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_payment_gateway_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול שערי תשלום.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_payment_gateways(
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת שערי תשלום מ-WooCommerce.
        
        Args:
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת שערי התשלום.
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
            response = await client.get("/payment_gateways")
            
            handle_response_error(response, "Failed to get payment gateways")
            return response.json()

    @mcp.tool()
    async def get_payment_gateway(
        gateway_id: str,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר שער תשלום בודד לפי המזהה שלו.
        
        Args:
            gateway_id: מזהה שער התשלום.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני שער התשלום.
        
        Examples:
            מזהים נפוצים של שערי תשלום: 'bacs' (העברה בנקאית), 'cheque' (המחאה), 
            'cod' (מזומן בעת אספקה), 'paypal' (PayPal), 'stripe' (Stripe) וכו'.
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
            response = await client.get(f"/payment_gateways/{gateway_id}")
            
            handle_response_error(response, f"Failed to get payment gateway {gateway_id}")
            return response.json()

    @mcp.tool()
    async def update_payment_gateway(
        gateway_id: str,
        gateway_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן שער תשלום קיים ב-WooCommerce.
        
        Args:
            gateway_id: מזהה שער התשלום.
            gateway_data: נתוני שער התשלום לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני שער התשלום המעודכן.
        
        Examples:
            >>> gateway_data = {
            ...     "enabled": True,
            ...     "title": "תשלום בהעברה בנקאית",
            ...     "description": "שלם באמצעות העברה בנקאית ישירה"
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
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.put(
                f"/payment_gateways/{gateway_id}",
                json=gateway_data
            )
            
            handle_response_error(response, f"Failed to update payment gateway {gateway_id}")
            return response.json() 