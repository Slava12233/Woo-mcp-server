"""
מודול לניהול קטגוריות מוצרים ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client

# ברירות מחדל למשתני סביבה יוגדרו בקובץ server.py

def register_product_category_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול קטגוריות מוצרים.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_product_categories(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת קטגוריות מוצרים מ-WooCommerce.
        
        Args:
            per_page: מספר קטגוריות לדף.
            page: מספר העמוד.
            filters: מסננים (שם, הורה וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת קטגוריות המוצרים.
        """
        # הערך יילקח מהמשתנים בזמן הקריאה לפונקציה
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
                "/products/categories",
                params=params
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                raise WordPressError(
                    error_data.get("message", "Failed to get product categories"),
                    error_data.get("code")
                )
            
            return response.json()
    
    @mcp.tool()
    async def get_product_category(
        category_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר קטגוריית מוצר בודדת לפי המזהה שלה.
        
        Args:
            category_id: מזהה הקטגוריה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקטגוריה.
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
            response = await client.get(f"/products/categories/{category_id}")
            
            if response.status_code >= 400:
                error_data = response.json()
                raise WordPressError(
                    error_data.get("message", f"Failed to get product category {category_id}"),
                    error_data.get("code")
                )
            
            return response.json()
    
    @mcp.tool()
    async def create_product_category(
        name: str,
        description: Optional[str] = None,
        parent: Optional[int] = None,
        image: Optional[Dict[str, str]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר קטגוריית מוצר חדשה ב-WooCommerce.
        
        Args:
            name: שם הקטגוריה.
            description: תיאור הקטגוריה.
            parent: מזהה של קטגוריית האב, אם קיימת.
            image: נתוני תמונת הקטגוריה, למשל {"src": "http://example.com/image.jpg"}.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקטגוריה שנוצרה.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        category_data = {
            "name": name
        }
        
        if description is not None:
            category_data["description"] = description
        
        if parent is not None:
            category_data["parent"] = parent
        
        if image is not None:
            category_data["image"] = image
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.post(
                "/products/categories",
                json=category_data
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                raise WordPressError(
                    error_data.get("message", "Failed to create product category"),
                    error_data.get("code")
                )
            
            return response.json()
    
    @mcp.tool()
    async def update_product_category(
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent: Optional[int] = None,
        image: Optional[Dict[str, str]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן קטגוריית מוצר קיימת ב-WooCommerce.
        
        Args:
            category_id: מזהה הקטגוריה.
            name: שם הקטגוריה החדש.
            description: תיאור הקטגוריה החדש.
            parent: מזהה של קטגוריית האב החדשה.
            image: נתוני תמונת הקטגוריה החדשים.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הקטגוריה המעודכנת.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_CONSUMER_KEY,
            DEFAULT_CONSUMER_SECRET,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        consumer_key = consumer_key or DEFAULT_CONSUMER_KEY
        consumer_secret = consumer_secret or DEFAULT_CONSUMER_SECRET
        
        category_data = {}
        
        if name is not None:
            category_data["name"] = name
        
        if description is not None:
            category_data["description"] = description
        
        if parent is not None:
            category_data["parent"] = parent
        
        if image is not None:
            category_data["image"] = image
        
        if not category_data:
            raise ValueError("At least one parameter must be provided for update")
        
        async with await create_wc_client(site_url, consumer_key, consumer_secret) as client:
            response = await client.put(
                f"/products/categories/{category_id}",
                json=category_data
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                raise WordPressError(
                    error_data.get("message", f"Failed to update product category {category_id}"),
                    error_data.get("code")
                )
            
            return response.json()
    
    @mcp.tool()
    async def delete_product_category(
        category_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק קטגוריית מוצר מ-WooCommerce.
        
        Args:
            category_id: מזהה הקטגוריה.
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
                f"/products/categories/{category_id}",
                params={"force": force}
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                raise WordPressError(
                    error_data.get("message", f"Failed to delete product category {category_id}"),
                    error_data.get("code")
                )
            
            return response.json() 