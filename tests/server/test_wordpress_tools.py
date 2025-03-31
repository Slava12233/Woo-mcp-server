"""
בדיקות לכלי ניהול WordPress
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_create_post_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי create_post רשום ועובד."""
    # יצירת תגובת HTTP מדומה - פוסט חדש
    mock_post_data = {
        "id": 1,
        "title": {
            "rendered": "כותרת לדוגמה"
        },
        "content": {
            "rendered": "תוכן לדוגמה"
        },
        "status": "draft"
    }
    mock_response = mock_http_response(json_data=mock_post_data)
    mock_wp_client.post.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_post", 
        {"title": "כותרת לדוגמה", "content": "תוכן לדוגמה", "status": "draft"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_posts_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי get_posts רשום ועובד."""
    # יצירת תגובת HTTP מדומה - רשימת פוסטים
    mock_posts_data = [
        {
            "id": 1,
            "title": {
                "rendered": "כותרת לדוגמה 1"
            },
            "status": "publish"
        },
        {
            "id": 2,
            "title": {
                "rendered": "כותרת לדוגמה 2"
            },
            "status": "draft"
        }
    ]
    mock_response = mock_http_response(json_data=mock_posts_data)
    mock_wp_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_posts", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_post_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי update_post רשום ועובד."""
    # יצירת תגובת HTTP מדומה - פוסט מעודכן
    mock_post_data = {
        "id": 1,
        "title": {
            "rendered": "כותרת מעודכנת"
        },
        "content": {
            "rendered": "תוכן לדוגמה"
        },
        "status": "publish"
    }
    mock_response = mock_http_response(json_data=mock_post_data)
    mock_wp_client.post.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_post", 
        {"post_id": 1, "title": "כותרת מעודכנת", "status": "publish"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_post_meta_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי get_post_meta רשום ועובד."""
    # יצירת תגובות HTTP מדומות
    mock_post_data = {
        "id": 1,
        "title": {
            "rendered": "כותרת לדוגמה"
        }
    }
    mock_post_response = mock_http_response(json_data=mock_post_data)
    
    mock_meta_data = [
        {"id": 1, "key": "meta_key_1", "value": "meta_value_1"},
        {"id": 2, "key": "meta_key_2", "value": "meta_value_2"}
    ]
    mock_meta_response = mock_http_response(json_data=mock_meta_data)
    
    # הגדרת תגובות ללקוח המדומה
    mock_wp_client.get.side_effect = [mock_post_response, mock_meta_response]
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_post_meta", {"post_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_post_meta_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי create_post_meta רשום ועובד."""
    # יצירת תגובת HTTP מדומה - מטא-דאטה חדש
    mock_meta_data = {"id": 3, "key": "new_meta_key", "value": "new_meta_value"}
    mock_response = mock_http_response(json_data=mock_meta_data)
    mock_wp_client.post.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "create_post_meta", 
        {"post_id": 1, "meta_key": "new_meta_key", "meta_value": "new_meta_value"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_post_meta_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי update_post_meta רשום ועובד."""
    # יצירת תגובת HTTP מדומה - מטא-דאטה מעודכן
    mock_meta_data = {"id": 1, "key": "meta_key_1", "value": "updated_value"}
    mock_response = mock_http_response(json_data=mock_meta_data)
    mock_wp_client.post.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_post_meta", 
        {"post_id": 1, "meta_id": 1, "meta_value": "updated_value"}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_post_meta_tool(mcp_tool_client, mock_wp_client, mock_http_response):
    """בדיקה שהכלי delete_post_meta רשום ועובד."""
    # יצירת תגובת HTTP מדומה - מחיקה מוצלחת
    mock_response = mock_http_response(json_data={"deleted": True})
    mock_wp_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "delete_post_meta", 
        {"post_id": 1, "meta_id": 1}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 