"""
בדיקות לכלי ניהול תגיות מוצרים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_product_tags_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_tags רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת תגיות מוצרים
    mock_tags = [
        {
            "id": 1,
            "name": "חדש",
            "slug": "new",
            "count": 5
        },
        {
            "id": 2,
            "name": "מומלץ",
            "slug": "featured",
            "count": 3
        }
    ]
    mock_response = mock_http_response(json_data=mock_tags)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_tags", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_tag_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_tag רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תגית מוצר
    mock_tag = {
        "id": 1,
        "name": "חדש",
        "slug": "new",
        "description": "מוצרים חדשים בחנות",
        "count": 5
    }
    mock_response = mock_http_response(json_data=mock_tag)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_tag", {"tag_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_tag_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_product_tag רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תגית שנוצרה
    mock_created_tag = {
        "id": 3,
        "name": "מבצע",
        "slug": "sale",
        "description": "מוצרים במבצע",
        "count": 0
    }
    mock_response = mock_http_response(json_data=mock_created_tag)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת התגית
    tag_data = {
        "name": "מבצע",
        "description": "מוצרים במבצע"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product_tag", {"tag_data": tag_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_tag_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_product_tag רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תגית מעודכנת
    mock_updated_tag = {
        "id": 1,
        "name": "חדש לגמרי",
        "slug": "brand-new",
        "description": "מוצרים חדשים לגמרי בחנות",
        "count": 5
    }
    mock_response = mock_http_response(json_data=mock_updated_tag)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון התגית
    tag_data = {
        "name": "חדש לגמרי",
        "slug": "brand-new",
        "description": "מוצרים חדשים לגמרי בחנות"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product_tag", 
        {"tag_id": 1, "tag_data": tag_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_tag_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_product_tag רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "name": "חדש",
        "slug": "new",
        "description": "מוצרים חדשים בחנות",
        "count": 5,
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_product_tag", {"tag_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 