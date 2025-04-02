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
from sse_starlette.sse import EventSourceResponse

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
    
    # הוספת נקודת קצה של MCP
    @api.get("/mcp")
    @api.post("/mcp")
    async def mcp_endpoint(request: Request):
        """נקודת הקצה של פרוטוקול MCP."""
        logger.info(f"MCP endpoint called with method: {request.method}")
        
        try:
            # לוג של headers כדי לראות מה נשלח
            headers_log = dict(request.headers)
            # הסרת פרטים רגישים מהלוג
            if 'authorization' in headers_log:
                headers_log['authorization'] = '[REDACTED]'
            if 'cookie' in headers_log:
                headers_log['cookie'] = '[REDACTED]'
                
            logger.info(f"Request headers: {headers_log}")
            
            # בדיקה אם זו בקשת SSE (בקשת GET עם header מתאים)
            accept_header = request.headers.get('accept', '')
            is_sse_request = request.method == 'GET' and 'text/event-stream' in accept_header
            
            if is_sse_request:
                logger.info("Handling SSE request")
                
                # יוצרים גנרטור ששולח עדכונים
                async def event_generator():
                    # שולחים הודעת פתיחה
                    yield {"event": "open", "data": "MCP server connection established"}
                    
                    # פה אפשר לשלוח עדכונים נוספים אם צריך
                    yield {"event": "capabilities", "data": "tools,roots"}
                    
                    # לתת תיאור של הכלים הזמינים
                    import json
                    tools_data = {
                        "tools": [
                            {"name": "get_products", "description": "Get WooCommerce products"},
                            {"name": "get_product_categories", "description": "Get WooCommerce product categories"},
                            {"name": "get_orders", "description": "Get WooCommerce orders"},
                            # וכו'
                        ]
                    }
                    yield {"event": "tools", "data": json.dumps(tools_data)}
                
                return EventSourceResponse(event_generator())
            else:
                # זוהי בקשת POST רגילה למסלול MCP
                # במקום להשתמש ב-handle_request שאינו קיים, נחזיר תיאור בסיסי של הכלים
                logger.info("Handling regular MCP request")
                
                # קריאת תוכן הבקשה
                body = await request.json() if request.method == 'POST' else {}
                logger.info(f"Request body: {body}")
                
                # החזרת תשובה בסיסית
                return {
                    "status": "ok",
                    "message": "MCP endpoint received request successfully",
                    "request_type": request.method,
                    "available_tools": ["get_products", "get_product_categories", "get_orders", "etc..."]
                }
                
        except Exception as e:
            logger.error(f"Error in MCP endpoint: {e}")
            logger.error(f"Error details: {traceback.format_exc()}")
            # החזרת שגיאה בפורמט מתאים
            return {"error": str(e)}
    
    # הוספת middleware לרישום כל הבקשות
    @api.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response
    
    # לשמור את ה-api באובייקט ה-mcp
    mcp.server = api
    
    # בדיקה שהשיטות הנדרשות קיימות
    logger.info(f"MCP object methods: {dir(mcp)}")
    logger.info(f"MCP server implementation: {mcp.server}")
    
    # הוספת מעטפת נוספת לנקודת הקצה של MCP
    app_mcp_path = "/mcp"
    logger.info(f"Setting up MCP endpoint at: {app_mcp_path}")
    
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