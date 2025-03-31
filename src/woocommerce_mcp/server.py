#!/usr/bin/env python3
"""
WooCommerce MCP Server - הנקודה הראשית של השרת
"""

import os
import asyncio
from dotenv import load_dotenv

# טעינת משתני סביבה מקובץ .env
load_dotenv()

from mcp.server.fastmcp import FastMCP

# קבלת פרטי התחברות מסביבת העבודה
DEFAULT_SITE_URL = os.environ.get("WORDPRESS_SITE_URL", "")
DEFAULT_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
DEFAULT_PASSWORD = os.environ.get("WORDPRESS_PASSWORD", "")
DEFAULT_CONSUMER_KEY = os.environ.get("WOOCOMMERCE_CONSUMER_KEY", "")
DEFAULT_CONSUMER_SECRET = os.environ.get("WOOCOMMERCE_CONSUMER_SECRET", "")

# ייצור שרת MCP
mcp = FastMCP("WooCommerce MCP Server")

def initialize():
    """רישום כל כלי ה-MCP."""
    # ייבוא המודולים
    from .wordpress import register_wordpress_tools
    from .products import register_product_tools
    from .product_categories import register_product_category_tools
    from .product_tags import register_product_tag_tools
    from .product_attributes import register_product_attribute_tools
    from .product_variations import register_product_variation_tools
    from .product_reviews import register_product_review_tools
    from .orders import register_order_tools
    from .order_refunds import register_order_refund_tools
    from .shipping_zones import register_shipping_zone_tools
    from .shipping_methods import register_shipping_method_tools
    from .taxes import register_tax_tools
    from .coupons import register_coupon_tools
    from .payment_gateways import register_payment_gateway_tools
    from .settings import register_settings_tools
    from .data import register_data_tools
    from .customers import register_customer_tools
    from .reports import register_report_tools
    
    # רישום הכלים
    register_wordpress_tools(mcp)
    register_product_tools(mcp)
    register_product_category_tools(mcp)
    register_product_tag_tools(mcp)
    register_product_attribute_tools(mcp)
    register_product_variation_tools(mcp)
    register_product_review_tools(mcp)
    register_order_tools(mcp)
    register_order_refund_tools(mcp)
    register_shipping_zone_tools(mcp)
    register_shipping_method_tools(mcp)
    register_tax_tools(mcp)
    register_coupon_tools(mcp)
    register_payment_gateway_tools(mcp)
    register_settings_tools(mcp)
    register_data_tools(mcp)
    register_customer_tools(mcp)
    register_report_tools(mcp)
    
    return mcp

async def main() -> None:
    """הפונקציה הראשית המפעילה את שרת ה-MCP."""
    # אתחול כל הכלים
    app = initialize()
    
    # הפעלת השרת
    app.run()

if __name__ == "__main__":
    asyncio.run(main()) 