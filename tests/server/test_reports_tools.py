"""
בדיקות לכלי ניהול דוחות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_sales_report_tool(mcp_tool_client, mock_wc_client, mock_sales_report, mock_http_response):
    """בדיקה שהכלי get_sales_report רשום ועובד."""
    # יצירת תגובת HTTP מדומה
    mock_response = mock_http_response(json_data=mock_sales_report)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_sales_report", {"period": "month"})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_products_report_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_products_report רשום ועובד."""
    # יצירת תגובת HTTP מדומה - דוח מוצרים
    mock_report_data = [
        {
            "product_id": 1,
            "items_sold": 10,
            "net_revenue": 499.90,
            "orders_count": 5
        },
        {
            "product_id": 2,
            "items_sold": 5,
            "net_revenue": 249.95,
            "orders_count": 3
        }
    ]
    mock_response = mock_http_response(json_data=mock_report_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "get_products_report", 
        {"period": "month", "per_page": 10, "page": 1}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_customers_report_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_customers_report רשום ועובד."""
    # יצירת תגובת HTTP מדומה - דוח לקוחות
    mock_report_data = [
        {
            "customer_id": 2,
            "orders_count": 5,
            "total_spend": 499.90
        },
        {
            "customer_id": 3,
            "orders_count": 3,
            "total_spend": 249.95
        }
    ]
    mock_response = mock_http_response(json_data=mock_report_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "get_customers_report", 
        {"per_page": 10, "page": 1}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_stock_report_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_stock_report רשום ועובד."""
    # יצירת תגובת HTTP מדומה - דוח מלאי
    mock_report_data = [
        {
            "product_id": 1,
            "stock_quantity": 15,
            "stock_status": "instock"
        },
        {
            "product_id": 2,
            "stock_quantity": 3,
            "stock_status": "instock"
        },
        {
            "product_id": 3,
            "stock_quantity": 0,
            "stock_status": "outofstock"
        }
    ]
    mock_response = mock_http_response(json_data=mock_report_data)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "get_stock_report", 
        {"per_page": 10, "page": 1}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 