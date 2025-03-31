"""
בדיקות לכלי ניהול וריאציות מוצרים
"""

import pytest
from unittest.mock import patch, AsyncMock

import mcp.types as types
from mcp.types import TextContent


@pytest.mark.anyio
async def test_get_product_variations_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_variations רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם רשימת וריאציות מוצר
    mock_variations = [
        {
            "id": 1,
            "regular_price": "99.99",
            "attributes": [
                {
                    "id": 6,
                    "name": "צבע",
                    "option": "אדום"
                }
            ]
        },
        {
            "id": 2,
            "regular_price": "99.99",
            "attributes": [
                {
                    "id": 6,
                    "name": "צבע",
                    "option": "כחול"
                }
            ]
        }
    ]
    mock_response = mock_http_response(json_data=mock_variations)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_variations", {"product_id": 123, "per_page": 10, "page": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_get_product_variation_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי get_product_variation רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני וריאציית מוצר
    mock_variation = {
        "id": 1,
        "regular_price": "99.99",
        "attributes": [
            {
                "id": 6,
                "name": "צבע",
                "option": "אדום"
            }
        ]
    }
    mock_response = mock_http_response(json_data=mock_variation)
    mock_wc_client.get.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("get_product_variation", {"product_id": 123, "variation_id": 1})
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_create_product_variation_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי create_product_variation רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני וריאציה שנוצרה
    mock_created_variation = {
        "id": 3,
        "regular_price": "109.99",
        "attributes": [
            {
                "id": 6,
                "name": "צבע",
                "option": "ירוק"
            }
        ]
    }
    mock_response = mock_http_response(json_data=mock_created_variation)
    mock_wc_client.post.return_value = mock_response
    
    # נתונים ליצירת הוריאציה
    variation_data = {
        "regular_price": "109.99",
        "attributes": [
            {
                "id": 6,
                "name": "צבע",
                "option": "ירוק"
            }
        ]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool("create_product_variation", {
        "product_id": 123,
        "variation_data": variation_data
    })
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_update_product_variation_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי update_product_variation רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם נתוני וריאציה מעודכנת
    mock_updated_variation = {
        "id": 1,
        "regular_price": "119.99",
        "attributes": [
            {
                "id": 6,
                "name": "צבע",
                "option": "אדום"
            }
        ]
    }
    mock_response = mock_http_response(json_data=mock_updated_variation)
    mock_wc_client.put.return_value = mock_response
    
    # נתונים לעדכון הוריאציה
    variation_data = {
        "regular_price": "119.99"
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "update_product_variation", 
        {
            "product_id": 123,
            "variation_id": 1,
            "variation_data": variation_data
        }
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_batch_update_product_variations_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי batch_update_product_variations רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת עדכון קבוצתי
    mock_batch_result = {
        "create": [
            {
                "id": 3,
                "regular_price": "109.99",
                "attributes": [
                    {
                        "id": 6,
                        "name": "צבע",
                        "option": "ירוק"
                    }
                ]
            }
        ],
        "update": [
            {
                "id": 1,
                "regular_price": "119.99"
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
                "regular_price": "109.99",
                "attributes": [
                    {
                        "id": 6,
                        "name": "צבע",
                        "option": "ירוק"
                    }
                ]
            }
        ],
        "update": [
            {
                "id": 1,
                "regular_price": "119.99"
            }
        ],
        "delete": [2]
    }
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "batch_update_product_variations", 
        {"product_id": 123, "batch_data": batch_data}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)


@pytest.mark.anyio
async def test_delete_product_variation_tool(mcp_tool_client, mock_wc_client, mock_http_response):
    """בדיקה שהכלי delete_product_variation רשום ועובד."""
    # יצירת תגובת HTTP מדומה עם תוצאת מחיקה
    mock_delete_result = {
        "id": 1,
        "regular_price": "99.99",
        "attributes": [
            {
                "id": 6,
                "name": "צבע",
                "option": "אדום"
            }
        ],
        "deleted": True
    }
    mock_response = mock_http_response(json_data=mock_delete_result)
    mock_wc_client.delete.return_value = mock_response
    
    # קריאה לכלי
    result = await mcp_tool_client.call_tool(
        "delete_product_variation", 
        {"product_id": 123, "variation_id": 1, "force": True}
    )
    
    # בדיקת התוצאה - אנחנו בודקים רק שהכלי רשום ועובד
    assert result is not None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent) 