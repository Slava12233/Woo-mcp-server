"""
מודול לניהול לקוחות ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error

def register_customer_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול לקוחות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_customers(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת לקוחות מ-WooCommerce.
        
        Args:
            per_page: מספר לקוחות לדף.
            page: מספר העמוד.
            filters: מסננים (דואר אלקטרוני, שם וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת הלקוחות.
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
                "/customers",
                params=params
            )
            
            handle_response_error(response, "Failed to get customers")
            return response.json()
    
    @mcp.tool()
    async def get_customer(
        customer_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר לקוח בודד לפי המזהה שלו.
        
        Args:
            customer_id: מזהה הלקוח.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הלקוח.
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
            response = await client.get(f"/customers/{customer_id}")
            
            handle_response_error(response, f"Failed to get customer {customer_id}")
            return response.json()
    
    @mcp.tool()
    async def create_customer(
        customer_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר לקוח חדש ב-WooCommerce.
        
        Args:
            customer_data: נתוני הלקוח (שם, דואר אלקטרוני, כתובת וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הלקוח שנוצר.
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
                "/customers",
                json=customer_data
            )
            
            handle_response_error(response, "Failed to create customer")
            return response.json()
    
    @mcp.tool()
    async def update_customer(
        customer_id: int,
        customer_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן לקוח קיים ב-WooCommerce.
        
        Args:
            customer_id: מזהה הלקוח.
            customer_data: נתוני הלקוח לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הלקוח המעודכן.
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
                f"/customers/{customer_id}",
                json=customer_data
            )
            
            handle_response_error(response, f"Failed to update customer {customer_id}")
            return response.json()
    
    @mcp.tool()
    async def delete_customer(
        customer_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק לקוח מ-WooCommerce.
        
        Args:
            customer_id: מזהה הלקוח.
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
                f"/customers/{customer_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete customer {customer_id}")
            return response.json()
            
    # מטא-דאטה של לקוחות
    @mcp.tool()
    async def get_customer_meta(
        customer_id: int,
        meta_key: Optional[str] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר מטא-דאטה של לקוח.
        
        Args:
            customer_id: מזהה הלקוח.
            meta_key: מפתח ספציפי של מטא-דאטה (אופציונלי).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה של הלקוח.
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
            response = await client.get(f"/customers/{customer_id}")
            
            handle_response_error(response, f"Failed to get customer {customer_id}")
            customer_data = response.json()
            
            meta_data = customer_data.get("meta_data", [])
            
            # אם מפתח ספציפי צוין, סנן רק את הערכים המתאימים
            if meta_key:
                meta_data = [item for item in meta_data if item.get("key") == meta_key]
                
            return meta_data
            
    @mcp.tool()
    async def create_customer_meta(
        customer_id: int,
        meta_key: str,
        meta_value: Any,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        יוצר או מעדכן מטא-דאטה של לקוח.
        
        Args:
            customer_id: מזהה הלקוח.
            meta_key: מפתח של מטא-דאטה.
            meta_value: ערך של מטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה מעודכנת של הלקוח.
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
            # קודם כל קבל את הלקוח הנוכחי
            response = await client.get(f"/customers/{customer_id}")
            
            handle_response_error(response, f"Failed to get customer {customer_id}")
            customer_data = response.json()
            
            # השג את המטא-דאטה הנוכחי
            meta_data = customer_data.get("meta_data", [])
            
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
            
            # שמור את השינויים בלקוח
            update_response = await client.put(
                f"/customers/{customer_id}",
                json={"meta_data": meta_data}
            )
            
            handle_response_error(update_response, f"Failed to update customer meta data for customer {customer_id}")
            updated_customer = update_response.json()
            
            return updated_customer.get("meta_data", []) 