"""
בדיקות לכלי ניהול קטגוריות מוצרים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_product_categories_tool(mcp_tool_client, mock_wc_client, mock_categories_list, mock_http_response):
    """בדיקה שהכלי get_product_categories רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_categories_list)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_categories", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_category_tool(mcp_tool_client, mock_wc_client, mock_category_data, mock_http_response):
    """בדיקה שהכלי get_product_category רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_category_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_category", {"category_id": 9})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_category_tool(mcp_tool_client, mock_wc_client, mock_category_data, mock_http_response):
    """בדיקה שהכלי create_product_category רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_category_data)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת קטגוריה
    category_data = {
        "name": "קטגוריה חדשה",
        "slug": "new-category",
        "parent": 0,
        "description": "תיאור של הקטגוריה"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product_category", {"category_data": category_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_category_tool(mcp_tool_client, mock_wc_client, mock_category_data, mock_http_response):
    """בדיקה שהכלי update_product_category רשום ועובד."""
    # יצירת תגובת HTTP מדומה - קטגוריה מעודכנת
    updated_category = mock_category_data.copy()
    updated_category["name"] = "קטגוריה מעודכנת"
    mock_response = mock_http_response(json_data=updated_category)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון קטגוריה
    category_data = {
        "name": "קטגוריה מעודכנת"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product_category", 
        {"category_id": 9, "category_data": category_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_category_tool(mcp_tool_client, mock_wc_client, mock_category_data, mock_http_response):
    """בדיקה שהכלי delete_product_category רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_category_data)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_product_category", {"category_id": 9, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 