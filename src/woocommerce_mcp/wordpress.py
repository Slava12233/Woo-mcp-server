"""
מודול לניהול פעולות בסיסיות של WordPress.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
import httpx

from .utils import WordPressError, create_wp_client, handle_response_error

def register_wordpress_tools(mcp: FastMCP) -> None:
    """
    רישום כלים לניהול פעולות WordPress בסיסיות.
    
    Args:
        mcp: אובייקט שרת ה-MCP.
    """
    
    @mcp.tool()
    async def create_post(
        title: str,
        content: str,
        status: str = "draft",
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר פוסט חדש ב-WordPress.
        
        Args:
            title: כותרת הפוסט.
            content: תוכן הפוסט.
            status: סטטוס הפוסט (draft, publish, וכו').
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הפוסט שנוצר.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.post(
                "/posts",
                json={
                    "title": title,
                    "content": content,
                    "status": status
                }
            )
            
            handle_response_error(response, "Failed to create post")
            return response.json()
    
    @mcp.tool()
    async def get_posts(
        per_page: int = 10,
        page: int = 1,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר רשימת פוסטים מ-WordPress.
        
        Args:
            per_page: מספר פוסטים לדף.
            page: מספר העמוד.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת הפוסטים.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.get(
                "/posts",
                params={
                    "per_page": per_page,
                    "page": page
                }
            )
            
            handle_response_error(response, "Failed to get posts")
            return response.json()
    
    @mcp.tool()
    async def update_post(
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן פוסט קיים ב-WordPress.
        
        Args:
            post_id: מזהה הפוסט.
            title: כותרת הפוסט החדשה (אופציונלי).
            content: תוכן הפוסט החדש (אופציונלי).
            status: סטטוס הפוסט החדש (אופציונלי).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני הפוסט המעודכן.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        post_data = {}
        if title is not None:
            post_data["title"] = title
        if content is not None:
            post_data["content"] = content
        if status is not None:
            post_data["status"] = status
        
        if not post_data:
            raise ValueError("At least one of title, content, or status must be provided")
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.post(
                f"/posts/{post_id}",
                json=post_data
            )
            
            handle_response_error(response, f"Failed to update post {post_id}")
            return response.json()
    
    @mcp.tool()
    async def get_post_meta(
        post_id: int,
        meta_key: Optional[str] = None,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        מחזיר מטא-דאטה של פוסט.
        
        Args:
            post_id: מזהה הפוסט.
            meta_key: מפתח ספציפי של מטא-דאטה (אופציונלי).
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            List[Dict[str, Any]]: רשימת מטא-דאטה של הפוסט.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            # קבל את הפוסט
            response = await client.get(f"/posts/{post_id}")
            
            handle_response_error(response, f"Failed to get post {post_id}")
            post_data = response.json()
            
            # קבל את המטא-דאטה
            if meta_key:
                # אם יש מפתח מטא-דאטה ספציפי, קבל רק אותו
                meta_response = await client.get(f"/posts/{post_id}/meta")
                handle_response_error(meta_response, f"Failed to get post meta for post {post_id}")
                
                all_meta = meta_response.json()
                return [item for item in all_meta if item.get("key") == meta_key]
            else:
                # אחרת, החזר את כל המטא-דאטה
                meta_response = await client.get(f"/posts/{post_id}/meta")
                handle_response_error(meta_response, f"Failed to get post meta for post {post_id}")
                
                return meta_response.json()
    
    @mcp.tool()
    async def create_post_meta(
        post_id: int,
        meta_key: str,
        meta_value: Any,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        יוצר מטא-דאטה חדש לפוסט.
        
        Args:
            post_id: מזהה הפוסט.
            meta_key: מפתח של מטא-דאטה.
            meta_value: ערך של מטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני המטא-דאטה שנוצר.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.post(
                f"/posts/{post_id}/meta",
                json={
                    "key": meta_key,
                    "value": meta_value
                }
            )
            
            handle_response_error(response, f"Failed to create meta for post {post_id}")
            return response.json()
    
    @mcp.tool()
    async def update_post_meta(
        post_id: int,
        meta_id: int,
        meta_value: Any,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מעדכן מטא-דאטה קיים של פוסט.
        
        Args:
            post_id: מזהה הפוסט.
            meta_id: מזהה המטא-דאטה.
            meta_value: ערך חדש של מטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: נתוני המטא-דאטה המעודכן.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.post(
                f"/posts/{post_id}/meta/{meta_id}",
                json={
                    "value": meta_value
                }
            )
            
            handle_response_error(response, f"Failed to update meta {meta_id} for post {post_id}")
            return response.json()
    
    @mcp.tool()
    async def delete_post_meta(
        post_id: int,
        meta_id: int,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        מוחק מטא-דאטה של פוסט.
        
        Args:
            post_id: מזהה הפוסט.
            meta_id: מזהה המטא-דאטה.
            site_url: כתובת האתר (אופציונלי אם מוגדר במשתני סביבה).
            username: שם משתמש ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
            password: סיסמה ל-WordPress (אופציונלי אם מוגדר במשתני סביבה).
        
        Returns:
            Dict[str, Any]: תוצאת המחיקה.
        """
        from .server import (
            DEFAULT_SITE_URL,
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
        )
        
        site_url = site_url or DEFAULT_SITE_URL
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        
        async with await create_wp_client(site_url, username, password) as client:
            response = await client.delete(f"/posts/{post_id}/meta/{meta_id}")
            
            handle_response_error(response, f"Failed to delete meta {meta_id} for post {post_id}")
            return response.json() 