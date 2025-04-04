#!/usr/bin/env python3
"""
WooCommerce MCP Server - הנקודה הראשית של השרת
"""

import os
import sys
import traceback
import logging
from dotenv import load_dotenv

# הגדרת לוגר
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("woocommerce-mcp")

# טעינת משתני סביבה מקובץ .env
logger.info("Loading environment variables...")
load_dotenv()

from mcp.server.fastmcp import FastMCP
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# קבלת פרטי התחברות מסביבת העבודה
DEFAULT_SITE_URL = os.environ.get("WORDPRESS_SITE_URL", "")
DEFAULT_USERNAME = os.environ.get("WORDPRESS_USERNAME", "")
DEFAULT_PASSWORD = os.environ.get("WORDPRESS_PASSWORD", "")
DEFAULT_CONSUMER_KEY = os.environ.get("WOOCOMMERCE_CONSUMER_KEY", "")
DEFAULT_CONSUMER_SECRET = os.environ.get("WOOCOMMERCE_CONSUMER_SECRET", "")

# הגדרות שרת
MCP_HOST = os.environ.get("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.environ.get("MCP_PORT", "8000"))

logger.info(f"Server configuration: HOST={MCP_HOST}, PORT={MCP_PORT}")

# ייצור שרת MCP
mcp = FastMCP("WooCommerce MCP Server")

def initialize():
    """רישום כל כלי ה-MCP."""
    logger.info("Initializing MCP tools...")
    
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
    
    logger.info("All MCP tools registered successfully")
    
    # הגדרת FastAPI לנקודות קצה בסיסיות
    api = FastAPI()
    
    # הוספת CORS middleware
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @api.get("/health")
    async def health_check():
        logger.info("Health check endpoint called")
        return {"status": "ok", "message": "WooCommerce MCP Server is running"}
        
    @api.get("/")
    async def root():
        logger.info("Root endpoint called")
        return {"message": "Welcome to WooCommerce MCP Server", "docs_url": "/docs"}
    
    # הוספת middleware לרישום כל הבקשות
    @api.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response
    
    return mcp

def main():
    """הפונקציה הראשית המפעילה את שרת ה-MCP."""
    try:
        logger.info(f"Starting WooCommerce MCP Server on {MCP_HOST}:{MCP_PORT}...")
        
        # אתחול כל הכלים
        app = initialize()
        
        # הדפסת מידע לדיאגנוסטיקה
        logger.info(f"Host: {MCP_HOST}")
        logger.info(f"Port: {MCP_PORT}")
        logger.info(f"WORDPRESS_SITE_URL: {'Set' if DEFAULT_SITE_URL else 'Not set'}")
        logger.info(f"WOOCOMMERCE_CONSUMER_KEY: {'Set' if DEFAULT_CONSUMER_KEY else 'Not set'}")
        logger.info(f"WOOCOMMERCE_CONSUMER_SECRET: {'Set' if DEFAULT_CONSUMER_SECRET else 'Not set'}")
        
        # חזרה לשימוש ישיר ב-uvicorn
        logger.info("Starting uvicorn server...")
        uvicorn.run(
            app.server, 
            host=MCP_HOST, 
            port=MCP_PORT,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 