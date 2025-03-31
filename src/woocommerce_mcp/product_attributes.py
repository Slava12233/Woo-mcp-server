"""
מודול לניהול תכונות מוצרים ותנאים שקשורים אליהם (Attribute Terms)
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_product_attribute_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול תכונות מוצרים ותנאי תכונות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    #
    # כלים לניהול תכונות מוצר
    #
    
    @mcp.tool()
    async def get_product_attributes(
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת תכונות מוצרים מ-WooCommerce.
        
        Args:
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת התכונות.
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
            response = await client.get("/products/attributes")
            
            handle_response_error(response, "Failed to get product attributes")
            return response.json()

    @mcp.tool()
    async def get_product_attribute(
        attribute_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר תכונת מוצר בודדת לפי המזהה שלה.
        
        Args:
            attribute_id: מזהה התכונה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התכונה.
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
            response = await client.get(f"/products/attributes/{attribute_id}")
            
            handle_response_error(response, f"Failed to get product attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def create_product_attribute(
        attribute_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר תכונת מוצר חדשה ב-WooCommerce.
        
        Args:
            attribute_data: נתוני התכונה (שם, סוג וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התכונה שנוצרה.
        
        Examples:
            >>> attribute_data = {
            ...     "name": "מידה",
            ...     "slug": "size",
            ...     "type": "select",
            ...     "order_by": "menu_order",
            ...     "has_archives": False
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
                "/products/attributes",
                json=attribute_data
            )
            
            handle_response_error(response, "Failed to create product attribute")
            return response.json()

    @mcp.tool()
    async def update_product_attribute(
        attribute_id: int,
        attribute_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן תכונת מוצר קיימת ב-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            attribute_data: נתוני התכונה לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התכונה המעודכנת.
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
                f"/products/attributes/{attribute_id}",
                json=attribute_data
            )
            
            handle_response_error(response, f"Failed to update product attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def delete_product_attribute(
        attribute_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק תכונת מוצר מ-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
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
                f"/products/attributes/{attribute_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete product attribute {attribute_id}")
            return response.json()
    
    #
    # כלים לניהול תנאי תכונות
    #
    
    @mcp.tool()
    async def get_attribute_terms(
        attribute_id: int,
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת תנאים של תכונת מוצר מ-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            per_page: מספר תנאים לדף.
            page: מספר העמוד.
            filters: מסננים נוספים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת התנאים.
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
                f"/products/attributes/{attribute_id}/terms",
                params=params
            )
            
            handle_response_error(response, f"Failed to get terms for attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def get_attribute_term(
        attribute_id: int,
        term_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר תנאי בודד של תכונת מוצר מ-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            term_id: מזהה התנאי.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התנאי.
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
            response = await client.get(f"/products/attributes/{attribute_id}/terms/{term_id}")
            
            handle_response_error(response, f"Failed to get term {term_id} for attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def create_attribute_term(
        attribute_id: int,
        term_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר תנאי חדש לתכונת מוצר ב-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            term_data: נתוני התנאי (שם, תיאור וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התנאי שנוצר.
        
        Examples:
            >>> term_data = {
            ...     "name": "גדול",
            ...     "slug": "large",
            ...     "description": "מידה גדולה"
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
                f"/products/attributes/{attribute_id}/terms",
                json=term_data
            )
            
            handle_response_error(response, f"Failed to create term for attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def update_attribute_term(
        attribute_id: int,
        term_id: int,
        term_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן תנאי קיים של תכונת מוצר ב-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            term_id: מזהה התנאי.
            term_data: נתוני התנאי לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני התנאי המעודכן.
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
                f"/products/attributes/{attribute_id}/terms/{term_id}",
                json=term_data
            )
            
            handle_response_error(response, f"Failed to update term {term_id} for attribute {attribute_id}")
            return response.json()

    @mcp.tool()
    async def delete_attribute_term(
        attribute_id: int,
        term_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק תנאי של תכונת מוצר ב-WooCommerce.
        
        Args:
            attribute_id: מזהה התכונה.
            term_id: מזהה התנאי.
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
                f"/products/attributes/{attribute_id}/terms/{term_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete term {term_id} for attribute {attribute_id}")
            return response.json() 