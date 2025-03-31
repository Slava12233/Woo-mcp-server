"""
מודול לניהול קופונים ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_coupon_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול קופונים.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_coupons(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת קופונים מ-WooCommerce.
        
        Args:
            per_page: מספר קופונים לדף.
            page: מספר העמוד.
            filters: מסננים (קוד, סטטוס, וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת הקופונים.
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
            response = await client.get(
                "/coupons",
                params=params
            )
            
            handle_response_error(response, "Failed to get coupons")
            return response.json()

    @mcp.tool()
    async def get_coupon(
        coupon_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר קופון בודד לפי המזהה שלו.
        
        Args:
            coupon_id: מזהה הקופון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקופון.
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
            response = await client.get(f"/coupons/{coupon_id}")
            
            handle_response_error(response, f"Failed to get coupon {coupon_id}")
            return response.json()

    @mcp.tool()
    async def create_coupon(
        coupon_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר קופון חדש ב-WooCommerce.
        
        Args:
            coupon_data: נתוני הקופון (קוד, סוג, ערך וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקופון שנוצר.
        
        Examples:
            >>> coupon_data = {
            ...     "code": "WELCOME10",
            ...     "discount_type": "percent",
            ...     "amount": "10",
            ...     "individual_use": True,
            ...     "exclude_sale_items": True,
            ...     "minimum_amount": "100.00"
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
        
        # ודא שיש קוד קופון
        if "code" not in coupon_data:
            raise ValueError("Coupon code is required")
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.post(
                "/coupons",
                json=coupon_data
            )
            
            handle_response_error(response, "Failed to create coupon")
            return response.json()

    @mcp.tool()
    async def update_coupon(
        coupon_id: int,
        coupon_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן קופון קיים ב-WooCommerce.
        
        Args:
            coupon_id: מזהה הקופון.
            coupon_data: נתוני הקופון לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקופון המעודכן.
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
                f"/coupons/{coupon_id}",
                json=coupon_data
            )
            
            handle_response_error(response, f"Failed to update coupon {coupon_id}")
            return response.json()

    @mcp.tool()
    async def delete_coupon(
        coupon_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק קופון מ-WooCommerce.
        
        Args:
            coupon_id: מזהה הקופון.
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
                f"/coupons/{coupon_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete coupon {coupon_id}")
            return response.json() 