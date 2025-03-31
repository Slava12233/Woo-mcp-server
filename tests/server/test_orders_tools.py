"""
בדיקות לכלי ניהול הזמנות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_orders_tool(mcp_tool_client, mock_wc_client, mock_orders_list, mock_http_response):
    """בדיקה שהכלי get_orders רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_orders_list)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_orders", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_order_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי get_order רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_order_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_order", {"order_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_order_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי create_order רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_order_data)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת הזמנה
    order_data = {
        "customer_id": 2,
        "status": "processing",
        "line_items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_order", {"order_data": order_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_order_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי update_order רשום ועובד."""
    # יצירת תגובת HTTP מדומה - הזמנה מעודכנת
    updated_order = mock_order_data.copy()
    updated_order["status"] = "completed"
    mock_response = mock_http_response(json_data=updated_order)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון הזמנה
    order_data = {
        "status": "completed"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_order", 
        {"order_id": 1, "order_data": order_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_order_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי delete_order רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_order_data)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_order", {"order_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_order_notes_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_order_notes רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_notes = [{"id": 1, "note": "הערה לדוגמה"}]
    mock_response = mock_http_response(json_data=mock_notes)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_order_notes", {"order_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_order_note_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_order_note רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_note = {"id": 2, "note": "הערה חדשה"}
    mock_response = mock_http_response(json_data=mock_note)
    mock_wc_client.post.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_order_note", 
        {"order_id": 1, "note": "הערה חדשה", "customer_note": False}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_order_meta_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי get_order_meta רשום ועובד."""
    # מוסיף מטא-דאטה להזמנה
    order_with_meta = mock_order_data.copy()
    order_with_meta["meta_data"] = [{"key": "test_key", "value": "test_value"}]
    
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=order_with_meta)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_order_meta", {"order_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_order_meta_tool(mcp_tool_client, mock_wc_client, mock_order_data, mock_http_response):
    """בדיקה שהכלי create_order_meta רשום ועובד."""
    # יצירת תגובות HTTP מדומות
    order_with_meta = mock_order_data.copy()
    order_with_meta["meta_data"] = [{"key": "test_key", "value": "test_value"}]
    mock_get_response = mock_http_response(json_data=order_with_meta)
    
    updated_order = order_with_meta.copy()
    updated_order["meta_data"].append({"key": "new_key", "value": "new_value"})
    mock_put_response = mock_http_response(json_data=updated_order)
    
    # הגדרת תגובות ללקוח המדומה
    mock_wc_client.get.return_value = mock_get_response
    mock_wc_client.put.return_value = mock_put_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_order_meta", 
        {"order_id": 1, "meta_key": "new_key", "meta_value": "new_value"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 