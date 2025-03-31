"""
בדיקות לכלי ניהול החזרים להזמנות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_order_refunds_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_order_refunds רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת החזרים
    mock_refunds = [
        {
            "id": 1,
            "date_created": "2023-01-15T12:00:00",
            "amount": "99.99",
            "reason": "מוצר פגום",
            "refunded_by": 1
        },
        {
            "id": 2,
            "date_created": "2023-01-20T14:30:00",
            "amount": "49.99",
            "reason": "שגיאה בהזמנה",
            "refunded_by": 1
        }
    ]
    mock_response = mock_http_response(json_data=mock_refunds)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_order_refunds", {"order_id": 123})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_order_refund_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_order_refund רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני החזר
    mock_refund = {
        "id": 1,
        "date_created": "2023-01-15T12:00:00",
        "amount": "99.99",
        "reason": "מוצר פגום",
        "refunded_by": 1,
        "line_items": [
            {
                "id": 1,
                "name": "מוצר לדוגמה",
                "product_id": 123,
                "quantity": 1,
                "subtotal": "99.99",
                "total": "99.99"
            }
        ]
    }
    mock_response = mock_http_response(json_data=mock_refund)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_order_refund", {"order_id": 123, "refund_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_order_refund_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_order_refund רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני החזר חדש
    mock_created_refund = {
        "id": 3,
        "date_created": "2023-01-25T10:15:00",
        "amount": "149.99",
        "reason": "לקוח ביטל הזמנה",
        "refunded_by": 1,
        "line_items": [
            {
                "id": 2,
                "name": "מוצר אחר",
                "product_id": 456,
                "quantity": 1,
                "subtotal": "149.99",
                "total": "149.99"
            }
        ]
    }
    mock_response = mock_http_response(json_data=mock_created_refund)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת החזר
    refund_data = {
        "amount": "149.99",
        "reason": "לקוח ביטל הזמנה",
        "line_items": [
            {
                "id": 2,
                "quantity": 1,
                "refund_total": 149.99
            }
        ]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_order_refund", {
        "order_id": 123,
        "refund_data": refund_data
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_order_refund_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_order_refund רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני החזר מעודכן
    mock_updated_refund = {
        "id": 1,
        "date_created": "2023-01-15T12:00:00",
        "amount": "99.99",
        "reason": "מוצר פגום - החלפה בוצעה",
        "refunded_by": 1
    }
    mock_response = mock_http_response(json_data=mock_updated_refund)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון החזר
    refund_data = {
        "reason": "מוצר פגום - החלפה בוצעה"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_order_refund", 
        {"order_id": 123, "refund_id": 1, "refund_data": refund_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_order_refund_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_order_refund רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "date_created": "2023-01-15T12:00:00",
        "amount": "99.99",
        "reason": "מוצר פגום",
        "refunded_by": 1,
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "delete_order_refund", 
        {"order_id": 123, "refund_id": 1, "force": True}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 