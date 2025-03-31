"""
מודול לניהול החזרות להזמנות ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_order_refund_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול החזרות להזמנות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_order_refunds(
        order_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת החזרות להזמנה מ-WooCommerce.
        
        Args:
            order_id: מזהה ההזמנה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת ההחזרות.
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
            response = await client.get(f"/orders/{order_id}/refunds")
            
            handle_response_error(response, f"Failed to get refunds for order {order_id}")
            return response.json()

    @mcp.tool()
    async def get_order_refund(
        order_id: int,
        refund_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר החזרה בודדת להזמנה לפי המזהה שלה.
        
        Args:
            order_id: מזהה ההזמנה.
            refund_id: מזהה ההחזרה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההחזרה.
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
            response = await client.get(f"/orders/{order_id}/refunds/{refund_id}")
            
            handle_response_error(response, f"Failed to get refund {refund_id} for order {order_id}")
            return response.json()

    @mcp.tool()
    async def create_order_refund(
        order_id: int,
        refund_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר החזרה חדשה להזמנה ב-WooCommerce.
        
        Args:
            order_id: מזהה ההזמנה.
            refund_data: נתוני ההחזרה (סכום, סיבה וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההחזרה שנוצרה.
        
        Examples:
            >>> refund_data = {
            ...     "amount": "50.00",
            ...     "reason": "פגם במוצר",
            ...     "line_items": [
            ...         {
            ...             "id": 123,
            ...             "quantity": 1,
            ...             "refund_total": 50.00
            ...         }
            ...     ]
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
        
        # ודא שיש סכום להחזרה
        if "amount" not in refund_data:
            raise ValueError("Refund amount is required")
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.post(
                f"/orders/{order_id}/refunds",
                json=refund_data
            )
            
            handle_response_error(response, f"Failed to create refund for order {order_id}")
            return response.json()

    @mcp.tool()
    async def delete_order_refund(
        order_id: int,
        refund_id: int,
        force: bool = True,  # החזרות בדרך כלל נמחקות לצמיתות
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק החזרה מהזמנה ב-WooCommerce.
        
        שים לב: מחיקת החזרה לא מבטלת את ההחזרה עצמה אם כבר בוצעה, אלא רק מוחקת את הרשומה.
        
        Args:
            order_id: מזהה ההזמנה.
            refund_id: מזהה ההחזרה.
            force: האם למחוק לצמיתות (אמת) או להעביר לפח (שקר).
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
            response = await client.delete(
                f"/orders/{order_id}/refunds/{refund_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete refund {refund_id} for order {order_id}")
            return response.json() 