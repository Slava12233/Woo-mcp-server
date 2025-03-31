"""
מודול לניהול הזמנות ב-WooCommerce.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wc_client, handle_response_error

def register_order_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול הזמנות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def get_orders(
        per_page: int = 10,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת הזמנות מ-WooCommerce.
        
        Args:
            per_page: מספר הזמנות לדף.
            page: מספר העמוד.
            filters: מסננים (סטטוס, תאריך וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת ההזמנות.
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
                "/orders",
                params=params
            )
            
            handle_response_error(response, "Failed to get orders")
            return response.json()
    
    @mcp.tool()
    async def get_order(
        order_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מחזיר הזמנה בודדת לפי המזהה שלה.
        
        Args:
            order_id: מזהה ההזמנה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההזמנה.
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
            response = await client.get(f"/orders/{order_id}")
            
            handle_response_error(response, f"Failed to get order {order_id}")
            return response.json()
    
    @mcp.tool()
    async def create_order(
        order_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר הזמנה חדשה ב-WooCommerce.
        
        Args:
            order_data: נתוני ההזמנה (פרטי לקוח, פריטים וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההזמנה שנוצרה.
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
                "/orders",
                json=order_data
            )
            
            handle_response_error(response, "Failed to create order")
            return response.json()
    
    @mcp.tool()
    async def update_order(
        order_id: int,
        order_data: Dict[str, Any],
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן הזמנה קיימת ב-WooCommerce.
        
        Args:
            order_id: מזהה ההזמנה.
            order_data: נתוני ההזמנה לעדכון.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההזמנה המעודכנת.
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
                f"/orders/{order_id}",
                json=order_data
            )
            
            handle_response_error(response, f"Failed to update order {order_id}")
            return response.json()
    
    @mcp.tool()
    async def delete_order(
        order_id: int,
        force: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק הזמנה מ-WooCommerce.
        
        Args:
            order_id: מזהה ההזמנה.
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
                f"/orders/{order_id}",
                params={"force": force}
            )
            
            handle_response_error(response, f"Failed to delete order {order_id}")
            return response.json()
    
    # הערות להזמנה
    @mcp.tool()
    async def get_order_notes(
        order_id: int,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר הערות להזמנה.
        
        Args:
            order_id: מזהה ההזמנה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת ההערות.
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
            response = await client.get(f"/orders/{order_id}/notes")
            
            handle_response_error(response, f"Failed to get notes for order {order_id}")
            return response.json()
    
    @mcp.tool()
    async def create_order_note(
        order_id: int,
        note: str,
        customer_note: bool = False,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר הערה חדשה להזמנה.
        
        Args:
            order_id: מזהה ההזמנה.
            note: תוכן ההערה.
            customer_note: האם ההערה מיועדת ללקוח (אמת) או רק למנהל (שקר).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני ההערה שנוצרה.
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
                f"/orders/{order_id}/notes",
                json={
                    "note": note,
                    "customer_note": customer_note
                }
            )
            
            handle_response_error(response, f"Failed to create note for order {order_id}")
            return response.json()
            
    # מטא-דאטה של הזמנות
    @mcp.tool()
    async def get_order_meta(
        order_id: int,
        meta_key: Optional[str] = None,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר מטא-דאטה של הזמנה.
        
        Args:
            order_id: מזהה ההזמנה.
            meta_key: מפתח ספציפי של מטא-דאטה (אופציונלי).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה של ההזמנה.
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
            response = await client.get(f"/orders/{order_id}")
            
            handle_response_error(response, f"Failed to get order {order_id}")
            order_data = response.json()
            
            meta_data = order_data.get("meta_data", [])
            
            # אם מפתח ספציפי צוין, סנן רק את הערכים המתאימים
            if meta_key:
                meta_data = [item for item in meta_data if item.get("key") == meta_key]
                
            return meta_data
            
    @mcp.tool()
    async def create_order_meta(
        order_id: int,
        meta_key: str,
        meta_value: Any,
        site_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        יוצר או מעדכן מטא-דאטה של הזמנה.
        
        Args:
            order_id: מזהה ההזמנה.
            meta_key: מפתח של מטא-דאטה.
            meta_value: ערך של מטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            consumer_key: מפתח צרכן (אופציונלי אם מוגדר במשתני סביבה).
            consumer_secret: מפתח סודי (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה מעודכנת של ההזמנה.
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
            # קודם כל קבל את ההזמנה הנוכחית
            response = await client.get(f"/orders/{order_id}")
            
            handle_response_error(response, f"Failed to get order {order_id}")
            order_data = response.json()
            
            # השג את המטא-דאטה הנוכחי
            meta_data = order_data.get("meta_data", [])
            
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
            
            # שמור את השינויים בהזמנה
            update_response = await client.put(
                f"/orders/{order_id}",
                json={"meta_data": meta_data}
            )
            
            handle_response_error(update_response, f"Failed to update order meta data for order {order_id}")
            updated_order = update_response.json()
            
            return updated_order.get("meta_data", []) 