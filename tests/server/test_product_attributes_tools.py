"""
בדיקות לכלי ניהול תכונות מוצרים ותנאי תכונות
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_product_attributes_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_attributes רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת תכונות מוצרים
    mock_attributes = [
        {
            "id": 1,
            "name": "צבע",
            "slug": "color",
            "type": "select",
            "order_by": "menu_order",
            "has_archives": False
        },
        {
            "id": 2,
            "name": "מידה",
            "slug": "size",
            "type": "select",
            "order_by": "menu_order",
            "has_archives": False
        }
    ]
    mock_response = mock_http_response(json_data=mock_attributes)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_attributes", {})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_attribute_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_attribute רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תכונת מוצר
    mock_attribute = {
        "id": 1,
        "name": "צבע",
        "slug": "color",
        "type": "select",
        "order_by": "menu_order",
        "has_archives": False
    }
    mock_response = mock_http_response(json_data=mock_attribute)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_attribute", {"attribute_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_attribute_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_product_attribute רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תכונה שנוצרה
    mock_created_attribute = {
        "id": 3,
        "name": "חומר",
        "slug": "material",
        "type": "select",
        "order_by": "menu_order",
        "has_archives": False
    }
    mock_response = mock_http_response(json_data=mock_created_attribute)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת התכונה
    attribute_data = {
        "name": "חומר",
        "type": "select",
        "order_by": "menu_order",
        "has_archives": False
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product_attribute", {"attribute_data": attribute_data})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_attribute_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_product_attribute רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תכונה מעודכנת
    mock_updated_attribute = {
        "id": 1,
        "name": "צבע מוצר",
        "slug": "product-color",
        "type": "select",
        "order_by": "name",
        "has_archives": True
    }
    mock_response = mock_http_response(json_data=mock_updated_attribute)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון התכונה
    attribute_data = {
        "name": "צבע מוצר",
        "slug": "product-color",
        "order_by": "name",
        "has_archives": True
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product_attribute", 
        {"attribute_id": 1, "attribute_data": attribute_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_attribute_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_product_attribute רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "name": "צבע",
        "slug": "color",
        "type": "select",
        "order_by": "menu_order",
        "has_archives": False,
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_product_attribute", {"attribute_id": 1, "force": True})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


# בדיקות לתנאי תכונות

@pytest.mark.anyio
async def test_get_attribute_terms_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_attribute_terms רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת תנאי תכונות
    mock_terms = [
        {
            "id": 1,
            "name": "אדום",
            "slug": "red",
            "count": 3
        },
        {
            "id": 2,
            "name": "כחול",
            "slug": "blue",
            "count": 5
        }
    ]
    mock_response = mock_http_response(json_data=mock_terms)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_attribute_terms", {
        "attribute_id": 1,
        "per_page": 10,
        "page": 1
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_attribute_term_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_attribute_term רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תנאי תכונה
    mock_term = {
        "id": 1,
        "name": "אדום",
        "slug": "red",
        "description": "צבע אדום",
        "count": 3
    }
    mock_response = mock_http_response(json_data=mock_term)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_attribute_term", {
        "attribute_id": 1,
        "term_id": 1
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_attribute_term_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_attribute_term רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תנאי תכונה שנוצר
    mock_created_term = {
        "id": 3,
        "name": "ירוק",
        "slug": "green",
        "description": "צבע ירוק",
        "count": 0
    }
    mock_response = mock_http_response(json_data=mock_created_term)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת התנאי
    term_data = {
        "name": "ירוק",
        "description": "צבע ירוק"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_attribute_term", {
        "attribute_id": 1,
        "term_data": term_data
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_attribute_term_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_attribute_term רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני תנאי תכונה מעודכן
    mock_updated_term = {
        "id": 1,
        "name": "אדום כהה",
        "slug": "dark-red",
        "description": "צבע אדום כהה",
        "count": 3
    }
    mock_response = mock_http_response(json_data=mock_updated_term)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון התנאי
    term_data = {
        "name": "אדום כהה",
        "slug": "dark-red",
        "description": "צבע אדום כהה"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("update_attribute_term", {
        "attribute_id": 1,
        "term_id": 1,
        "term_data": term_data
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_attribute_term_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_attribute_term רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "name": "אדום",
        "slug": "red",
        "description": "צבע אדום",
        "count": 3,
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("delete_attribute_term", {
        "attribute_id": 1,
        "term_id": 1,
        "force": True
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 