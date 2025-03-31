"""
בדיקות לכלי ניהול קופונים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_coupons_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_coupons רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת קופונים
    mock_coupons = [
        {
            "id": 1,
            "code": "WELCOME10",
            "discount_type": "percent",
            "amount": "10",
            "date_created": "2023-01-15T12:00:00",
            "usage_count": 5
        },
        {
            "id": 2,
            "code": "SUMMER20",
            "discount_type": "percent",
            "amount": "20",
            "date_created": "2023-01-20T14:30:00",
            "usage_count": 3
        }
    ]
    mock_response = mock_http_response(json_data=mock_coupons)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_coupons", {"per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_coupon_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_coupon רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני קופון
    mock_coupon = {
        "id": 1,
        "code": "WELCOME10",
        "discount_type": "percent",
        "amount": "10",
        "date_created": "2023-01-15T12:00:00",
        "date_expires": None,
        "usage_limit": 100,
        "usage_limit_per_user": 1,
        "usage_count": 5,
        "individual_use": True,
        "product_ids": [],
        "excluded_product_ids": [],
        "minimum_amount": "0",
        "maximum_amount": "0"
    }
    mock_response = mock_http_response(json_data=mock_coupon)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_coupon", {"coupon_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_coupon_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_coupon רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני קופון חדש
    mock_created_coupon = {
        "id": 3,
        "code": "FALL15",
        "discount_type": "percent",
        "amount": "15",
        "date_created": "2023-01-25T10:15:00",
        "date_expires": "2023-10-01T00:00:00",
        "usage_limit": 50,
        "usage_limit_per_user": 1,
        "usage_count": 0,
        "individual_use": True,
        "product_ids": [123, 456],
        "excluded_product_ids": [],
        "minimum_amount": "100",
        "maximum_amount": "0"
    }
    mock_response = mock_http_response(json_data=mock_created_coupon)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת קופון
    coupon_data = {
        "code": "FALL15",
        "discount_type": "percent",
        "amount": "15",
        "date_expires": "2023-10-01T00:00:00",
        "usage_limit": 50,
        "usage_limit_per_user": 1,
        "individual_use": True,
        "product_ids": [123, 456],
        "minimum_amount": "100"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_coupon", {"coupon_data": coupon_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_coupon_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_coupon רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני קופון מעודכן
    mock_updated_coupon = {
        "id": 1,
        "code": "WELCOME10",
        "discount_type": "percent",
        "amount": "15",
        "date_created": "2023-01-15T12:00:00",
        "date_expires": "2023-12-31T00:00:00",
        "usage_limit": 100,
        "usage_limit_per_user": 1,
        "usage_count": 5,
        "individual_use": True,
        "product_ids": [],
        "excluded_product_ids": [],
        "minimum_amount": "0",
        "maximum_amount": "0"
    }
    mock_response = mock_http_response(json_data=mock_updated_coupon)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון קופון
    coupon_data = {
        "amount": "15",
        "date_expires": "2023-12-31T00:00:00"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_coupon", 
        {"coupon_id": 1, "coupon_data": coupon_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_coupon_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_coupon רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "code": "WELCOME10",
        "discount_type": "percent",
        "amount": "10",
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_coupon", {"coupon_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_batch_update_coupons_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי batch_update_coupons רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת עדכון קבוצתי
    mock_batch_result = {
        "create": [
            {
                "id": 3,
                "code": "FALL15",
                "discount_type": "percent",
                "amount": "15"
            }
        ],
        "update": [
            {
                "id": 1,
                "code": "WELCOME10",
                "amount": "15"
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
                "code": "FALL15",
                "discount_type": "percent",
                "amount": "15"
            }
        ],
        "update": [
            {
                "id": 1,
                "amount": "15"
            }
        ],
        "delete": [2]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("batch_update_coupons", {"batch_data": batch_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 