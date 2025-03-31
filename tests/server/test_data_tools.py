"""
בדיקות לכלי ניהול נתונים כלליים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_countries_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_countries רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מדינות
    mock_countries = [
        {
            "code": "IL",
            "name": "ישראל"
        },
        {
            "code": "US",
            "name": "ארצות הברית (ארה\"ב)"
        },
        {
            "code": "GB",
            "name": "בריטניה (UK)"
        }
    ]
    mock_response = mock_http_response(json_data=mock_countries)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_countries", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_country_states_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_country_states רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מדינות
    mock_states = [
        {
            "code": "CA",
            "name": "קליפורניה"
        },
        {
            "code": "NY",
            "name": "ניו יורק"
        },
        {
            "code": "TX",
            "name": "טקסס"
        }
    ]
    mock_response = mock_http_response(json_data=mock_states)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_country_states", {"country": "US"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_currencies_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_currencies רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת מטבעות
    mock_currencies = [
        {
            "code": "ILS",
            "name": "שקל חדש",
            "symbol": "₪"
        },
        {
            "code": "USD",
            "name": "דולר אמריקאי",
            "symbol": "$"
        },
        {
            "code": "EUR",
            "name": "אירו",
            "symbol": "€"
        }
    ]
    mock_response = mock_http_response(json_data=mock_currencies)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_currencies", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_currency_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_currency רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני מטבע
    mock_currency = {
        "code": "ILS",
        "name": "שקל חדש",
        "symbol": "₪"
    }
    mock_response = mock_http_response(json_data=mock_currency)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_currency", {"currency": "ILS"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_current_currency_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_current_currency רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני המטבע הנוכחי
    mock_current_currency = {
        "code": "ILS",
        "name": "שקל חדש",
        "symbol": "₪"
    }
    mock_response = mock_http_response(json_data=mock_current_currency)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_current_currency", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 