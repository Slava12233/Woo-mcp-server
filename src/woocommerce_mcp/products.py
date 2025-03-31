"""
מודול לניהול מוצרים ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error


def register_product_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול מוצרים.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_products(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת מוצרים מ-WooCommerce.
        
        Args:
            per_page: מספר מוצרים לדף.
            page: מספר העמוד.
            filters: מסננים (קטגוריה, סטטוס וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת המוצרים.
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
                "/products",
                params=params
            )
            
            handle_response_error(response, "Failed to get products")
            return response.json()

    @mcp.tool()
    async def get_product(
        product_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר מוצר בודד לפי המזהה שלו.
        
        Args:
            product_id: מזהה המוצר.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני המוצר.
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
            response = await client.get(f"/products/{product_id}")
            
            handle_response_error(response, f"Failed to get product {product_id}")
            return response.json()

    @mcp.tool()
    async def create_product(
        product_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר מוצר חדש ב-WooCommerce.
        
        Args:
            product_data: נתוני המוצר (שם, מחיר, תיאור וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני המוצר שנוצר.
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
                "/products",
                json=product_data
            )
            
            handle_response_error(response, "Failed to create product")
            return response.json()

    @mcp.tool()
    async def update_product(
        product_id: int,
        product_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן מוצר קיים ב-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
            product_data: נתוני המוצר לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני המוצר המעודכן.
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
                f"/products/{product_id}",
                json=product_data
            )
            
            handle_response_error(response, f"Failed to update product {product_id}")
            return response.json()

    @mcp.tool()
    async def delete_product(
        product_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק מוצר מ-WooCommerce.
        
        Args:
            product_id: מזהה המוצר.
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
                f"/products/{product_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete product {product_id}")
            return response.json()
            
    # מטא-דאטה של מוצרים
    @mcp.tool()
    async def get_product_meta(
        product_id: int,
        meta_key: Optional[str] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר מטא-דאטה של מוצר.
        
        Args:
            product_id: מזהה המוצר.
            meta_key: מפתח ספציפי של מטא-דאטה (אופציונלי).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה של המוצר.
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
            response = await client.get(f"/products/{product_id}")
            
            handle_response_error(response, f"Failed to get product {product_id}")
            product_data = response.json()
            
            meta_data = product_data.get("meta_data", [])
            
            # אם מפתח ספציפי צוין, סנן רק את הערכים המתאימים
            if meta_key:
                meta_data = [item for item in meta_data if item.get("key") == meta_key]
                
            return meta_data
            
    @mcp.tool()
    async def create_product_meta(
        product_id: int,
        meta_key: str,
        meta_value: Any,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        יוצר או מעדכן מטא-דאטה של מוצר.
        
        Args:
            product_id: מזהה המוצר.
            meta_key: מפתח של מטא-דאטה.
            meta_value: ערך של מטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה מעודכנת של המוצר.
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
            # קודם כל קבל את המוצר הנוכחי
            response = await client.get(f"/products/{product_id}")
            
            handle_response_error(response, f"Failed to get product {product_id}")
            product_data = response.json()
            
            # השג את המטא-דאטה הנוכחי
            meta_data = product_data.get("meta_data", [])
            
            # חפש אם המפתח כבר קיים
            existing_meta_index = next((i for i, item in enumerate(meta_data) 
                                      if item.get("key") == meta_key), None)
            
            if existing_meta_index is not None:
                # עדכן את הערך הקיים
                meta_data[existing_meta_index]["value"] = meta_value
            else:
                # הוסף ערך חדש
                meta_data.append({
                    "key": meta_key,
                    "value": meta_value
                })
            
            # שמור את השינויים במוצר
            update_response = await client.put(
                f"/products/{product_id}",
                json={"meta_data": meta_data}
            )
            
            handle_response_error(update_response, f"Failed to update product meta data for product {product_id}")
            updated_product = update_response.json()
            
            return updated_product.get("meta_data", [])
            
    @mcp.tool()
    async def delete_product_meta(
        product_id: int,
        meta_key: str,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מוחק מטא-דאטה של מוצר.
        
        Args:
            product_id: מזהה המוצר.
            meta_key: מפתח של מטא-דאטה למחיקה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה מעודכנת של המוצר.
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
            # קודם כל קבל את המוצר הנוכחי
            response = await client.get(f"/products/{product_id}")
            
            handle_response_error(response, f"Failed to get product {product_id}")
            product_data = response.json()
            
            # השג את המטא-דאטה הנוכחי
            meta_data = product_data.get("meta_data", [])
            
            # סנן החוצה את המפתח שצריך למחוק
            updated_meta_data = [item for item in meta_data if item.get("key") != meta_key]
            
            # שמור את השינויים במוצר
            update_response = await client.put(
                f"/products/{product_id}",
                json={"meta_data": updated_meta_data}
            )
            
            handle_response_error(update_response, f"Failed to delete product meta data for product {product_id}")
            updated_product = update_response.json()
            
            return updated_product.get("meta_data", []) 