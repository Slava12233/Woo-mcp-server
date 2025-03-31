"""
בדיקות לכלי ניהול לקוחות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_customers_tool(mcp_tool_client, mock_wc_client, mock_customers_list, mock_http_response):
    """בדיקה שהכלי get_customers רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_customers_list)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_customers", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_customer_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי get_customer רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_customer_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_customer", {"customer_id": 2})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_customer_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי create_customer רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_customer_data)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת לקוח
    customer_data = {
        "email": "new@example.com",
        "first_name": "משה",
        "last_name": "לוי",
        "username": "moshe",
        "password": "password123"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_customer", {"customer_data": customer_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_customer_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי update_customer רשום ועובד."""
    # יצירת תגובת HTTP מדומה - לקוח מעודכן
    updated_customer = mock_customer_data.copy()
    updated_customer["first_name"] = "משה"
    mock_response = mock_http_response(json_data=updated_customer)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון לקוח
    customer_data = {
        "first_name": "משה"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_customer", 
        {"customer_id": 2, "customer_data": customer_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_customer_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי delete_customer רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_customer_data)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_customer", {"customer_id": 2, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_customer_meta_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי get_customer_meta רשום ועובד."""
    # מוסיף מטא-דאטה ללקוח
    customer_with_meta = mock_customer_data.copy()
    customer_with_meta["meta_data"] = [{"key": "test_key", "value": "test_value"}]
    
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=customer_with_meta)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_customer_meta", {"customer_id": 2})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_customer_meta_tool(mcp_tool_client, mock_wc_client, mock_customer_data, mock_http_response):
    """בדיקה שהכלי create_customer_meta רשום ועובד."""
    # יצירת תגובות HTTP מדומות
    customer_with_meta = mock_customer_data.copy()
    customer_with_meta["meta_data"] = [{"key": "test_key", "value": "test_value"}]
    mock_get_response = mock_http_response(json_data=customer_with_meta)
    
    updated_customer = customer_with_meta.copy()
    updated_customer["meta_data"].append({"key": "new_key", "value": "new_value"})
    mock_put_response = mock_http_response(json_data=updated_customer)
    
    # הגדרת תגובות ללקוח המדומה
    mock_wc_client.get.return_value = mock_get_response
    mock_wc_client.put.return_value = mock_put_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_customer_meta", 
        {"customer_id": 2, "meta_key": "new_key", "meta_value": "new_value"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 