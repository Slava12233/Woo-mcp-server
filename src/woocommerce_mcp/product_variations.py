"""
מודול לניהול וריאציות מוצרים ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_product_variation_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול וריאציות מוצרים.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_product_variations(
        product_id: int,
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת וריאציות של מוצר מ-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
            per_page: מספר וריאציות לדף.
            page: מספר העמוד.
            filters: מסננים (סטטוס וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת הוריאציות.
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
                f"/products/{product_id}/variations",
                params=params
            )
            
            handle_response_error(response, f"Failed to get variations for product {product_id}")
            return response.json()

    @mcp.tool()
    async def get_product_variation(
        product_id: int,
        variation_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר וריאציית מוצר בודדת לפי המזהה שלה.
        
        Args:
            product_id: מזהה המוצר.
            variation_id: מזהה הוריאציה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הוריאציה.
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
            response = await client.get(f"/products/{product_id}/variations/{variation_id}")
            
            handle_response_error(response, f"Failed to get variation {variation_id} for product {product_id}")
            return response.json()

    @mcp.tool()
    async def create_product_variation(
        product_id: int,
        variation_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר וריאציית מוצר חדשה ב-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
            variation_data: נתוני הוריאציה (מחיר, מלאי, תכונות וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הוריאציה שנוצרה.
        
        Examples:
            >>> variation_data = {
            ...     "regular_price": "99.99",
            ...     "attributes": [
            ...         {
            ...             "id": 1,
            ...             "option": "גדול"
            ...         }
            ...     ],
            ...     "stock_quantity": 10
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
            response = await client.post(
                f"/products/{product_id}/variations",
                json=variation_data
            )
            
            handle_response_error(response, f"Failed to create variation for product {product_id}")
            return response.json()

    @mcp.tool()
    async def update_product_variation(
        product_id: int,
        variation_id: int,
        variation_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן וריאציית מוצר קיימת ב-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
            variation_id: מזהה הוריאציה.
            variation_data: נתוני הוריאציה לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הוריאציה המעודכנת.
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
                f"/products/{product_id}/variations/{variation_id}",
                json=variation_data
            )
            
            handle_response_error(response, f"Failed to update variation {variation_id} for product {product_id}")
            return response.json()

    @mcp.tool()
    async def delete_product_variation(
        product_id: int,
        variation_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק וריאציית מוצר מ-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
            variation_id: מזהה הוריאציה.
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
                f"/products/{product_id}/variations/{variation_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete variation {variation_id} for product {product_id}")
            return response.json() 