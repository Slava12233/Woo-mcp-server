"""
בדיקות לכלי ניהול חוות דעת מוצרים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_product_reviews_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_reviews רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת חוות דעת
    mock_reviews = [
        {
            "id": 1,
            "product_id": 123,
            "reviewer": "ישראל ישראלי",
            "reviewer_email": "israel@example.com",
            "review": "מוצר מצוין!",
            "rating": 5,
            "status": "approved",
            "date_created": "2023-01-15T12:00:00"
        },
        {
            "id": 2,
            "product_id": 456,
            "reviewer": "שרה כהן",
            "reviewer_email": "sarah@example.com",
            "review": "מוצר טוב, אבל יקר מדי",
            "rating": 3,
            "status": "approved",
            "date_created": "2023-01-20T14:30:00"
        }
    ]
    mock_response = mock_http_response(json_data=mock_reviews)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_reviews", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_review_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_review רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני חוות דעת
    mock_review = {
        "id": 1,
        "product_id": 123,
        "reviewer": "ישראל ישראלי",
        "reviewer_email": "israel@example.com",
        "review": "מוצר מצוין!",
        "rating": 5,
        "status": "approved",
        "date_created": "2023-01-15T12:00:00"
    }
    mock_response = mock_http_response(json_data=mock_review)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_review", {"review_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_review_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_product_review רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני חוות דעת חדשה
    mock_created_review = {
        "id": 3,
        "product_id": 789,
        "reviewer": "יוסי לוי",
        "reviewer_email": "yossi@example.com",
        "review": "שירות מהיר ומוצר איכותי",
        "rating": 4,
        "status": "approved",
        "date_created": "2023-01-25T10:15:00"
    }
    mock_response = mock_http_response(json_data=mock_created_review)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת חוות דעת
    review_data = {
        "product_id": 789,
        "reviewer": "יוסי לוי",
        "reviewer_email": "yossi@example.com",
        "review": "שירות מהיר ומוצר איכותי",
        "rating": 4
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product_review", {"review_data": review_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_review_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_product_review רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני חוות דעת מעודכנת
    mock_updated_review = {
        "id": 1,
        "product_id": 123,
        "reviewer": "ישראל ישראלי",
        "reviewer_email": "israel@example.com",
        "review": "מוצר מצוין! מומלץ מאוד!",
        "rating": 5,
        "status": "approved",
        "date_created": "2023-01-15T12:00:00"
    }
    mock_response = mock_http_response(json_data=mock_updated_review)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון חוות דעת
    review_data = {
        "review": "מוצר מצוין! מומלץ מאוד!"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product_review", 
        {"review_id": 1, "review_data": review_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_review_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_product_review רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "product_id": 123,
        "reviewer": "ישראל ישראלי",
        "reviewer_email": "israel@example.com",
        "review": "מוצר מצוין!",
        "rating": 5,
        "status": "approved",
        "date_created": "2023-01-15T12:00:00",
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_product_review", {"review_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 