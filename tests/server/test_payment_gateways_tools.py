"""
בדיקות לכלי ניהול שערי תשלום
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_payment_gateways_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_payment_gateways רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת שערי תשלום
    mock_gateways = [
        {
            "id": "bacs",
            "title": "העברה בנקאית",
            "description": "בצע תשלום ישירות לחשבון הבנק שלנו.",
            "order": 0,
            "enabled": True,
            "method_title": "העברה בנקאית",
            "method_description": "מאפשר תשלומים באמצעות BACS. נדרש גם ממך לאשר את ההזמנה באופן ידני."
        },
        {
            "id": "cheque",
            "title": "תשלום בצ'ק",
            "description": "שלם באמצעות צ'ק.",
            "order": 1,
            "enabled": True,
            "method_title": "תשלום בצ'ק",
            "method_description": "מאפשר תשלום בצ'ק. נדרש גם ממך לאשר את ההזמנה באופן ידני."
        }
    ]
    mock_response = mock_http_response(json_data=mock_gateways)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_payment_gateways", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_payment_gateway_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_payment_gateway רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שער תשלום
    mock_gateway = {
        "id": "bacs",
        "title": "העברה בנקאית",
        "description": "בצע תשלום ישירות לחשבון הבנק שלנו.",
        "order": 0,
        "enabled": True,
        "method_title": "העברה בנקאית",
        "method_description": "מאפשר תשלומים באמצעות BACS. נדרש גם ממך לאשר את ההזמנה באופן ידני.",
        "settings": {
            "title": {
                "id": "title",
                "label": "כותרת",
                "description": "זו מופיעה בעגלה ובקופה.",
                "type": "text",
                "value": "העברה בנקאית",
                "default": "העברה בנקאית",
                "tip": "זו מופיעה בעגלה ובקופה.",
                "placeholder": ""
            },
            "instructions": {
                "id": "instructions",
                "label": "הוראות",
                "description": "ההוראות שיתווספו לדף \"תודה\".",
                "type": "textarea",
                "value": "",
                "default": "",
                "tip": "ההוראות שיתווספו לדף \"תודה\".",
                "placeholder": ""
            }
        }
    }
    mock_response = mock_http_response(json_data=mock_gateway)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_payment_gateway", {"gateway_id": "bacs"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_payment_gateway_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_payment_gateway רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני שער תשלום מעודכן
    mock_updated_gateway = {
        "id": "bacs",
        "title": "העברה בנקאית ישירה",
        "description": "בצע תשלום ישירות לחשבון הבנק שלנו לטיפול מהיר יותר.",
        "order": 0,
        "enabled": True,
        "method_title": "העברה בנקאית",
        "method_description": "מאפשר תשלומים באמצעות BACS. נדרש גם ממך לאשר את ההזמנה באופן ידני.",
        "settings": {
            "title": {
                "id": "title",
                "value": "העברה בנקאית ישירה"
            },
            "instructions": {
                "id": "instructions",
                "value": "העבר תשלום לחשבון 12345 בבנק לאומי."
            }
        }
    }
    mock_response = mock_http_response(json_data=mock_updated_gateway)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון שער תשלום
    gateway_data = {
        "title": "העברה בנקאית ישירה",
        "description": "בצע תשלום ישירות לחשבון הבנק שלנו לטיפול מהיר יותר.",
        "settings": {
            "instructions": "העבר תשלום לחשבון 12345 בבנק לאומי."
        }
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_payment_gateway", 
        {"gateway_id": "bacs", "gateway_data": gateway_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 