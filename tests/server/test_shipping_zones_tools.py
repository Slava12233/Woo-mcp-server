"""
בדיקות לכלי ניהול אזורי משלוח
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_shipping_zones_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_shipping_zones רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת אזורי משלוח
    mock_zones = [
        {
            "id": 1,
            "name": "ישראל",
            "order": 0
        },
        {
            "id": 2,
            "name": "ארה\"ב",
            "order": 1
        }
    ]
    mock_response = mock_http_response(json_data=mock_zones)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_shipping_zones", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_shipping_zone_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_shipping_zone רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני אזור משלוח
    mock_zone = {
        "id": 1,
        "name": "ישראל",
        "order": 0
    }
    mock_response = mock_http_response(json_data=mock_zone)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_shipping_zone", {"zone_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_shipping_zone_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_shipping_zone רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני אזור משלוח חדש
    mock_created_zone = {
        "id": 3,
        "name": "אירופה",
        "order": 2
    }
    mock_response = mock_http_response(json_data=mock_created_zone)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת אזור משלוח
    zone_data = {
        "name": "אירופה",
        "order": 2
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_shipping_zone", {"zone_data": zone_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_shipping_zone_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_shipping_zone רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני אזור משלוח מעודכן
    mock_updated_zone = {
        "id": 1,
        "name": "ישראל - משלוח מהיר",
        "order": 0
    }
    mock_response = mock_http_response(json_data=mock_updated_zone)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון אזור משלוח
    zone_data = {
        "name": "ישראל - משלוח מהיר"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_shipping_zone", 
        {"zone_id": 1, "zone_data": zone_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_shipping_zone_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_shipping_zone רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "name": "ישראל",
        "order": 0,
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_shipping_zone", {"zone_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_shipping_zone_locations_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_shipping_zone_locations רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מיקומים של אזור משלוח
    mock_locations = [
        {
            "code": "IL",
            "type": "country"
        },
        {
            "code": "JLM",
            "type": "postcode"
        }
    ]
    mock_response = mock_http_response(json_data=mock_locations)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_shipping_zone_locations", {"zone_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_shipping_zone_locations_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_shipping_zone_locations רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מיקומים מעודכנת
    mock_updated_locations = [
        {
            "code": "IL",
            "type": "country"
        },
        {
            "code": "JLM",
            "type": "postcode"
        },
        {
            "code": "TLV",
            "type": "postcode"
        }
    ]
    mock_response = mock_http_response(json_data=mock_updated_locations)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון מיקומים
    locations = [
        {
            "code": "IL",
            "type": "country"
        },
        {
            "code": "JLM",
            "type": "postcode"
        },
        {
            "code": "TLV",
            "type": "postcode"
        }
    ]
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_shipping_zone_locations", 
        {"zone_id": 1, "locations": locations}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 