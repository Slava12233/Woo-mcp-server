"""
בדיקות לכלי ניהול מוצרים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_products_tool(mcp_tool_client, mock_wc_client, mock_products_list, mock_http_response):
    """בדיקה שהכלי get_products רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_products_list)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_products", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי get_product רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_product_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product", {"product_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי create_product רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_product_data)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת מוצר
    product_data = {
        "name": "מוצר חדש",
        "type": "simple",
        "regular_price": "99.99",
        "description": "תיאור של המוצר"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product", {"product_data": product_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי update_product רשום ועובד."""
    # יצירת תגובת HTTP מדומה - מוצר מעודכן
    updated_product = mock_product_data.copy()
    updated_product["name"] = "מוצר מעודכן"
    mock_response = mock_http_response(json_data=updated_product)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון מוצר
    product_data = {
        "name": "מוצר מעודכן"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product", 
        {"product_id": 1, "product_data": product_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי delete_product רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_product_data)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_product", {"product_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_meta_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי get_product_meta רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_product_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_meta", {"product_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_meta_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי create_product_meta רשום ועובד."""
    # יצירת תגובות HTTP מדומות
    mock_get_response = mock_http_response(json_data=mock_product_data)
    
    updated_product = mock_product_data.copy()
    updated_product["meta_data"].append({
        "key": "new_meta_key",
        "value": "new_meta_value"
    })
    mock_put_response = mock_http_response(json_data=updated_product)
    
    # הגדרת תגובות ללקוח המדומה
    mock_wc_client.get.return_value = mock_get_response
    mock_wc_client.put.return_value = mock_put_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_product_meta", 
        {"product_id": 1, "meta_key": "new_meta_key", "meta_value": "new_meta_value"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_meta_tool(mcp_tool_client, mock_wc_client, mock_product_data, mock_http_response):
    """בדיקה שהכלי delete_product_meta רשום ועובד."""
    # יצירת תגובות HTTP מדומות
    mock_get_response = mock_http_response(json_data=mock_product_data)
    
    updated_product = mock_product_data.copy()
    updated_product["meta_data"] = []
    mock_put_response = mock_http_response(json_data=updated_product)
    
    # הגדרת תגובות ללקוח המדומה
    mock_wc_client.get.return_value = mock_get_response
    mock_wc_client.put.return_value = mock_put_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "delete_product_meta", 
        {"product_id": 1, "meta_key": "test_meta_key"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 