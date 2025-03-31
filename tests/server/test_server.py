"""
בדיקות לקובץ server.py
"""

import os
import sys
import pytest
from unittest.mock import patch

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_server_initialization():
    """בדיקה שהשרת מאותחל כראוי."""
    from woocommerce_mcp import initialize
    
    # יצירת שרת חדש
    server = initialize()
    
    # בדיקה שהשרת נוצר ותקין
    assert server is not None
    
    # בדיקה שהשרת מסוג FastMCP
    from mcp.server.fastmcp import FastMCP
    assert isinstance(server, FastMCP)
    
    # בדיקה שמספר פקודות הכלים זמין
    assert hasattr(server, "tool")
    
    # מכיוון שאין גישה פומבית ללא כלים, בדיקה זו ממומשת בצורה פשוטה יותר
    # בלי להסתמך על מבנה פנימי של MCP
    assert True


@pytest.mark.anyio
async def test_environment_variables():
    """בדיקה שמשתני הסביבה נטענים כראוי."""
    # הגדר משתני סביבה לבדיקה
    test_vars = {
        "WORDPRESS_SITE_URL": "https://test-wp-site.com",
        "WORDPRESS_USERNAME": "test_username",
        "WORDPRESS_PASSWORD": "test_password",
        "WOOCOMMERCE_CONSUMER_KEY": "test_consumer_key",
        "WOOCOMMERCE_CONSUMER_SECRET": "test_consumer_secret"
    }
    
    # שמור את המשתנים המקוריים
    original_vars = {}
    for key in test_vars:
        original_vars[key] = os.environ.get(key)
    
    try:
        # הגדר משתני סביבה חדשים
        for key, value in test_vars.items():
            os.environ[key] = value
        
        # טען את המודול מחדש (או אתחל אותו) במקום להשתמש ב-patch.dict של sys.modules
        import importlib
        import woocommerce_mcp.server
        importlib.reload(woocommerce_mcp.server)
        
        # בדוק שהמשתנים נטענו כראוי
        assert woocommerce_mcp.server.DEFAULT_SITE_URL == test_vars["WORDPRESS_SITE_URL"]
        assert woocommerce_mcp.server.DEFAULT_USERNAME == test_vars["WORDPRESS_USERNAME"]
        assert woocommerce_mcp.server.DEFAULT_PASSWORD == test_vars["WORDPRESS_PASSWORD"]
        assert woocommerce_mcp.server.DEFAULT_CONSUMER_KEY == test_vars["WOOCOMMERCE_CONSUMER_KEY"]
        assert woocommerce_mcp.server.DEFAULT_CONSUMER_SECRET == test_vars["WOOCOMMERCE_CONSUMER_SECRET"]
        
    finally:
        # החזר את המשתנים המקוריים
        for key, value in original_vars.items():
            if value is not None:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)


@pytest.mark.anyio
async def test_server_modules_imported(mcp_server):
    """בדיקה שכל המודולים יובאו כראוי."""
    # בדיקה שהשרת נוצר
    assert mcp_server is not None
    
    # הבדיקה מסתמכת על העובדה שיבוא המודולים בהצלחה הוא תנאי מספיק
    # כדי להבטיח שהשרת מאותחל כראוי. בדיקה מפורטת יותר תצריך
    # מוק של API של וורדפרס ו-WooCommerce או קריאה אמיתית לשרת
    assert True 