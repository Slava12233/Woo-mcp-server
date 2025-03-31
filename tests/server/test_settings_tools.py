"""
בדיקות לכלי ניהול הגדרות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_settings_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_settings רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת הגדרות
    mock_settings = [
        {
            "id": "woocommerce_currency",
            "label": "מטבע",
            "description": "זוהי המטבע שבה מוצרים בחנות שלך מתומחרים.",
            "type": "select",
            "default": "ILS",
            "options": {
                "ILS": "₪ שקל חדש",
                "USD": "$ דולר אמריקאי"
            },
            "value": "ILS"
        },
        {
            "id": "woocommerce_currency_pos",
            "label": "מיקום סמל המטבע",
            "description": "זה קובע את מיקום סמל המטבע.",
            "type": "select",
            "default": "right",
            "options": {
                "left": "שמאל (₪99.99)",
                "right": "ימין (99.99₪)",
                "left_space": "שמאל עם רווח (₪ 99.99)",
                "right_space": "ימין עם רווח (99.99 ₪)"
            },
            "value": "right"
        }
    ]
    mock_response = mock_http_response(json_data=mock_settings)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_settings", {"group": "general"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_setting_option_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_setting_option רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני הגדרה ספציפית
    mock_setting = {
        "id": "woocommerce_currency",
        "label": "מטבע",
        "description": "זוהי המטבע שבה מוצרים בחנות שלך מתומחרים.",
        "type": "select",
        "default": "ILS",
        "options": {
            "ILS": "₪ שקל חדש",
            "USD": "$ דולר אמריקאי"
        },
        "value": "ILS"
    }
    mock_response = mock_http_response(json_data=mock_setting)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_setting_option", {
        "group": "general", 
        "option_id": "woocommerce_currency"
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_setting_option_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_setting_option רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני הגדרה מעודכנת
    mock_updated_setting = {
        "id": "woocommerce_currency",
        "label": "מטבע",
        "description": "זוהי המטבע שבה מוצרים בחנות שלך מתומחרים.",
        "type": "select",
        "default": "ILS",
        "options": {
            "ILS": "₪ שקל חדש",
            "USD": "$ דולר אמריקאי"
        },
        "value": "USD"
    }
    mock_response = mock_http_response(json_data=mock_updated_setting)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון הגדרה
    setting_data = {
        "value": "USD"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_setting_option", 
        {
            "group": "general", 
            "option_id": "woocommerce_currency", 
            "setting_data": setting_data
        }
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_batch_update_settings_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי batch_update_settings רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת עדכון קבוצתי
    mock_batch_result = [
        {
            "id": "woocommerce_currency",
            "label": "מטבע",
            "value": "USD"
        },
        {
            "id": "woocommerce_currency_pos",
            "label": "מיקום סמל המטבע",
            "value": "left"
        }
    ]
    mock_response = mock_http_response(json_data=mock_batch_result)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים לעדכון קבוצתי
    settings_data = [
        {
            "id": "woocommerce_currency",
            "value": "USD"
        },
        {
            "id": "woocommerce_currency_pos",
            "value": "left"
        }
    ]
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "batch_update_settings", 
        {"group": "general", "settings_data": settings_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_system_status_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_system_status רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני סטטוס מערכת
    mock_status = {
        "environment": {
            "home_url": "https://example.com",
            "wordpress_version": "6.0",
            "woocommerce_version": "7.0.0",
            "php_version": "8.0.0"
        },
        "database": {
            "wc_database_version": "7.0.0",
            "database_prefix": "wp_"
        },
        "active_plugins": [
            {
                "plugin": "woocommerce/woocommerce.php",
                "name": "WooCommerce",
                "version": "7.0.0",
                "active": True
            }
        ],
        "theme": {
            "name": "Storefront",
            "version": "4.1.0",
            "child_theme": False
        }
    }
    mock_response = mock_http_response(json_data=mock_status)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_system_status", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_system_status_tools_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_system_status_tools רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת כלי סטטוס מערכת
    mock_status_tools = [
        {
            "id": "clear_transients",
            "name": "ניקוי טרנזיאנטים",
            "action": "clear",
            "description": "מנקה את הטרנזיאנטים של WooCommerce",
            "success": True,
            "failure": False
        },
        {
            "id": "clear_expired_transients",
            "name": "ניקוי טרנזיאנטים פגי תוקף",
            "action": "clear",
            "description": "מנקה את הטרנזיאנטים פגי התוקף של WooCommerce",
            "success": True,
            "failure": False
        }
    ]
    mock_response = mock_http_response(json_data=mock_status_tools)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_system_status_tools", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_execute_system_status_tool_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי execute_system_status_tool רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת הפעלת כלי סטטוס
    mock_tool_result = {
        "id": "clear_transients",
        "name": "ניקוי טרנזיאנטים",
        "action": "clear",
        "description": "מנקה את הטרנזיאנטים של WooCommerce",
        "success": True,
        "message": "פעולה הושלמה בהצלחה",
        "failure": False
    }
    mock_response = mock_http_response(json_data=mock_tool_result)
    mock_wc_client.put.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "execute_system_status_tool", 
        {"tool_id": "clear_transients"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 