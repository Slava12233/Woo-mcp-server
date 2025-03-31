"""
בדיקות לכלי ניהול מיסים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_tax_classes_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_tax_classes רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מחלקות מס
    mock_tax_classes = [
        {
            "slug": "standard",
            "name": "סטנדרטי"
        },
        {
            "slug": "reduced-rate",
            "name": "מופחת"
        }
    ]
    mock_response = mock_http_response(json_data=mock_tax_classes)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_tax_classes", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_tax_class_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_tax_class רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני מחלקת מס חדשה
    mock_created_tax_class = {
        "slug": "zero-rate",
        "name": "מע\"מ אפס"
    }
    mock_response = mock_http_response(json_data=mock_created_tax_class)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת מחלקת מס
    tax_class_data = {
        "name": "מע\"מ אפס"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_tax_class", {"tax_class_data": tax_class_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_tax_class_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_tax_class רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "slug": "zero-rate",
        "name": "מע\"מ אפס",
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_tax_class", {"slug": "zero-rate", "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_tax_rates_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_tax_rates רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת שיעורי מס
    mock_tax_rates = [
        {
            "id": 1,
            "country": "IL",
            "state": "",
            "postcode": "",
            "city": "",
            "rate": "17.0000",
            "name": "מע\"מ",
            "priority": 1,
            "compound": False,
            "shipping": True,
            "order": 0,
            "class": "standard"
        },
        {
            "id": 2,
            "country": "IL",
            "state": "",
            "postcode": "",
            "city": "",
            "rate": "0.0000",
            "name": "מע\"מ אפס",
            "priority": 1,
            "compound": False,
            "shipping": True,
            "order": 0,
            "class": "zero-rate"
        }
    ]
    mock_response = mock_http_response(json_data=mock_tax_rates)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_tax_rates", {"class": "standard"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_tax_rate_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_tax_rate רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיעור מס
    mock_tax_rate = {
        "id": 1,
        "country": "IL",
        "state": "",
        "postcode": "",
        "city": "",
        "rate": "17.0000",
        "name": "מע\"מ",
        "priority": 1,
        "compound": False,
        "shipping": True,
        "order": 0,
        "class": "standard"
    }
    mock_response = mock_http_response(json_data=mock_tax_rate)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_tax_rate", {"rate_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_tax_rate_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_tax_rate רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיעור מס חדש
    mock_created_tax_rate = {
        "id": 3,
        "country": "US",
        "state": "CA",
        "postcode": "",
        "city": "",
        "rate": "7.2500",
        "name": "מס מכירות קליפורניה",
        "priority": 1,
        "compound": False,
        "shipping": True,
        "order": 0,
        "class": "standard"
    }
    mock_response = mock_http_response(json_data=mock_created_tax_rate)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת שיעור מס
    tax_rate_data = {
        "country": "US",
        "state": "CA",
        "rate": "7.25",
        "name": "מס מכירות קליפורניה",
        "class": "standard"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_tax_rate", {"tax_rate_data": tax_rate_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_tax_rate_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_tax_rate רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שיעור מס מעודכן
    mock_updated_tax_rate = {
        "id": 1,
        "country": "IL",
        "state": "",
        "postcode": "",
        "city": "",
        "rate": "17.5000",
        "name": "מע\"מ עדכני",
        "priority": 1,
        "compound": False,
        "shipping": True,
        "order": 0,
        "class": "standard"
    }
    mock_response = mock_http_response(json_data=mock_updated_tax_rate)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון שיעור מס
    tax_rate_data = {
        "rate": "17.50",
        "name": "מע\"מ עדכני"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_tax_rate", 
        {"rate_id": 1, "tax_rate_data": tax_rate_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_tax_rate_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_tax_rate רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "country": "IL",
        "rate": "17.0000",
        "name": "מע\"מ",
        "class": "standard",
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_tax_rate", {"rate_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_batch_update_tax_rates_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי batch_update_tax_rates רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת עדכון קבוצתי
    mock_batch_result = {
        "create": [
            {
                "id": 4,
                "country": "EU",
                "rate": "20.0000",
                "name": "מע\"מ אירופאי",
                "class": "standard"
            }
        ],
        "update": [
            {
                "id": 1,
                "country": "IL",
                "rate": "17.5000",
                "name": "מע\"מ עדכני",
                "class": "standard"
            }
        ],
        "delete": [2]
    }
    mock_response = mock_http_response(json_data=mock_batch_result)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים לעדכון קבוצתי
    batch_data = {
        "create": [
            {
                "country": "EU",
                "rate": "20.00",
                "name": "מע\"מ אירופאי",
                "class": "standard"
            }
        ],
        "update": [
            {
                "id": 1,
                "rate": "17.50",
                "name": "מע\"מ עדכני"
            }
        ],
        "delete": [2]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("batch_update_tax_rates", {"batch_data": batch_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 