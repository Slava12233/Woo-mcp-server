"""
בדיקות לכלי ניהול שיטות משלוח
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_shipping_methods_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_shipping_methods רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת שיטות משלוח
    mock_methods = [
        {
            "id": "flat_rate",
            "title": "תעריף קבוע",
            "description": "תעריף קבוע למשלוח"
        },
        {
            "id": "free_shipping",
            "title": "משלוח חינם",
            "description": "משלוח חינם עבור הזמנות מעל סכום מסוים"
        }
    ]
    mock_response = mock_http_response(json_data=mock_methods)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_shipping_methods", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_zone_shipping_methods_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_zone_shipping_methods רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת שיטות משלוח לאזור
    mock_zone_methods = [
        {
            "id": 1,
            "instance_id": 1,
            "title": "תעריף קבוע",
            "order": 1,
            "enabled": True,
            "method_id": "flat_rate",
            "settings": {
                "cost": {
                    "id": "cost",
                    "label": "עלות",
                    "value": "10"
                }
            }
        },
        {
            "id": 2,
            "instance_id": 2,
            "title": "משלוח חינם",
            "order": 2,
            "enabled": True,
            "method_id": "free_shipping",
            "settings": {
                "min_amount": {
                    "id": "min_amount",
                    "label": "מינימום סכום הזמנה",
                    "value": "200"
                }
            }
        }
    ]
    mock_response = mock_http_response(json_data=mock_zone_methods)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_zone_shipping_methods", {"zone_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_zone_shipping_method_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_zone_shipping_method רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיטת משלוח באזור
    mock_zone_method = {
        "id": 1,
        "instance_id": 1,
        "title": "תעריף קבוע",
        "order": 1,
        "enabled": True,
        "method_id": "flat_rate",
        "settings": {
            "cost": {
                "id": "cost",
                "label": "עלות",
                "value": "10"
            }
        }
    }
    mock_response = mock_http_response(json_data=mock_zone_method)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_zone_shipping_method", {"zone_id": 1, "instance_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_zone_shipping_method_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_zone_shipping_method רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיטת משלוח חדשה
    mock_created_method = {
        "id": 3,
        "instance_id": 3,
        "title": "משלוח בינלאומי",
        "order": 3,
        "enabled": True,
        "method_id": "flat_rate",
        "settings": {
            "cost": {
                "id": "cost",
                "label": "עלות",
                "value": "50"
            }
        }
    }
    mock_response = mock_http_response(json_data=mock_created_method)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת שיטת משלוח
    method_data = {
        "method_id": "flat_rate",
        "settings": {
            "cost": "50",
            "title": "משלוח בינלאומי"
        }
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_zone_shipping_method", {
        "zone_id": 1, 
        "method_data": method_data
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_zone_shipping_method_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_zone_shipping_method רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיטת משלוח מעודכנת
    mock_updated_method = {
        "id": 1,
        "instance_id": 1,
        "title": "תעריף קבוע - מבצע",
        "order": 1,
        "enabled": True,
        "method_id": "flat_rate",
        "settings": {
            "cost": {
                "id": "cost",
                "label": "עלות",
                "value": "5"
            }
        }
    }
    mock_response = mock_http_response(json_data=mock_updated_method)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון שיטת משלוח
    method_data = {
        "settings": {
            "cost": "5",
            "title": "תעריף קבוע - מבצע"
        }
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_zone_shipping_method", 
        {"zone_id": 1, "instance_id": 1, "method_data": method_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_zone_shipping_method_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_zone_shipping_method רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "instance_id": 1,
        "title": "תעריף קבוע",
        "method_id": "flat_rate",
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "delete_zone_shipping_method", 
        {"zone_id": 1, "instance_id": 1, "force": True}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 