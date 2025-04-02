from flask import Flask, Response, request, jsonify, stream_with_context
from flask_cors import CORS
import json
import time
import threading
import queue
import os
import logging

# הגדרת לוגר
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# מפה של חיבורים פתוחים ותורי הודעות
clients = {}

@app.route('/')
def health_check():
    """בדיקת בריאות פשוטה"""
    logger.info("Health check requested")
    return jsonify({"status": "ok", "message": "MCP Server is running"})

@app.route('/mcp')
def mcp_endpoint():
    """נקודת קצה עם תמיכה ב-SSE"""
    client_id = request.args.get('client_id') or str(time.time())
    logger.info(f"New SSE connection established for client {client_id}")
    
    # יוצר תור הודעות ייעודי לכל לקוח
    client_queue = queue.Queue()
    clients[client_id] = client_queue
    
    def generate():
        try:
            # שולח אירוע מוכנות
            logger.info(f"Sending ready event to client {client_id}")
            yield 'event: ready\ndata: {}\n\n'
            
            # לולאה שמחכה להודעות בתור ושולחת אותן
            while True:
                try:
                    # מנסה לקבל הודעה מהתור עם טיימאאוט
                    message = client_queue.get(timeout=25)
                    logger.debug(f"Sending message to client {client_id}: {message[:50]}...")
                    yield message
                except queue.Empty:
                    # אם אין הודעות, שולח keep-alive
                    logger.debug(f"Sending keep-alive to client {client_id}")
                    yield ': keep-alive\n\n'
        finally:
            # כשהחיבור נסגר, מוחק את התור
            logger.info(f"Connection closed for client {client_id}")
            if client_id in clients:
                del clients[client_id]
    
    response = Response(stream_with_context(generate()), 
                       content_type='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

@app.route('/mcp', methods=['POST'])
def mcp_function_call():
    """מטפל בקריאות פונקציה"""
    data = request.json
    client_id = request.args.get('client_id')
    
    logger.info(f"Function call received from client {client_id if client_id else 'unknown'}: {str(data)[:100]}...")
    
    if not data:
        logger.error("No data provided in function call")
        return jsonify({"error": "No data provided"}), 400
    
    function_name = data.get('function')
    params = data.get('params', {})
    
    # מטפל בפונקציה
    result = handle_mcp_function(function_name, params)
    
    # שולח את התשובה כאירוע SSE אם קיים client_id
    if client_id and client_id in clients:
        message = f'event: function_call_result\ndata: {json.dumps({"function": function_name, "result": result})}\n\n'
        clients[client_id].put(message)
        logger.info(f"Result sent to client {client_id} via SSE")
    
    # מחזיר גם תשובת HTTP רגילה
    logger.info(f"Returning HTTP response for function {function_name}")
    return jsonify({
        "function": function_name,
        "result": result
    })

def handle_mcp_function(function_name, params):
    """מטפל בפונקציות של ה-MCP"""
    logger.info(f"Handling function: {function_name} with params: {params}")
    
    # פונקציות WooCommerce
    if function_name == 'list_products':
        return woo_list_products(params)
    elif function_name == 'get_product':
        return woo_get_product(params)
    elif function_name == 'create_product':
        return woo_create_product(params)
    elif function_name == 'update_product':
        return woo_update_product(params)
    elif function_name == 'delete_product':
        return woo_delete_product(params)
    elif function_name == 'list_orders':
        return woo_list_orders(params)
    elif function_name == 'get_order':
        return woo_get_order(params)
    elif function_name == 'get_customer':
        return woo_get_customer(params)
    elif function_name == 'tools_list':
        return get_available_tools()
    
    logger.warning(f"Function {function_name} not supported")
    return {"error": f"Function {function_name} not supported"}

# פונקציות WooCommerce
def woo_list_products(params):
    """רשימת מוצרים מ-WooCommerce"""
    logger.info("Listing WooCommerce products")
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "products": [
            {"id": 1, "name": "מוצר לדוגמה 1", "price": "100"},
            {"id": 2, "name": "מוצר לדוגמה 2", "price": "200"},
            {"id": 3, "name": "מוצר לדוגמה 3", "price": "300"}
        ]
    }

def woo_get_product(params):
    """מידע על מוצר ספציפי"""
    product_id = params.get('id')
    logger.info(f"Getting WooCommerce product {product_id}")
    
    if not product_id:
        return {"error": "Product ID is required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "product": {
            "id": product_id,
            "name": f"מוצר {product_id}",
            "price": "100",
            "description": "תיאור המוצר לדוגמה",
            "stock": 10
        }
    }

def woo_create_product(params):
    """יצירת מוצר חדש"""
    logger.info(f"Creating new WooCommerce product: {params.get('name', 'unknown')}")
    
    # בדיקת פרמטרים חובה
    name = params.get('name')
    price = params.get('price')
    
    if not name or not price:
        return {"error": "Product name and price are required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "product": {
            "id": 999,  # בדרך כלל נוצר על ידי WooCommerce
            "name": name,
            "price": price,
            "description": params.get('description', ''),
            "created": True
        }
    }

def woo_update_product(params):
    """עדכון מוצר קיים"""
    product_id = params.get('id')
    logger.info(f"Updating WooCommerce product {product_id}")
    
    if not product_id:
        return {"error": "Product ID is required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "product": {
            "id": product_id,
            "updated": True,
            "changes": params
        }
    }

def woo_delete_product(params):
    """מחיקת מוצר"""
    product_id = params.get('id')
    logger.info(f"Deleting WooCommerce product {product_id}")
    
    if not product_id:
        return {"error": "Product ID is required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "deleted": True,
        "id": product_id
    }

def woo_list_orders(params):
    """רשימת הזמנות"""
    logger.info("Listing WooCommerce orders")
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "orders": [
            {"id": 101, "total": "150", "status": "processing"},
            {"id": 102, "total": "250", "status": "completed"},
            {"id": 103, "total": "350", "status": "pending"}
        ]
    }

def woo_get_order(params):
    """מידע על הזמנה ספציפית"""
    order_id = params.get('id')
    logger.info(f"Getting WooCommerce order {order_id}")
    
    if not order_id:
        return {"error": "Order ID is required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "order": {
            "id": order_id,
            "date": "2025-04-02",
            "customer": "לקוח לדוגמה",
            "total": "199.99",
            "status": "processing",
            "items": [
                {"product_id": 1, "name": "מוצר 1", "quantity": 2},
                {"product_id": 3, "name": "מוצר 3", "quantity": 1}
            ]
        }
    }

def woo_get_customer(params):
    """מידע על לקוח"""
    customer_id = params.get('id')
    logger.info(f"Getting WooCommerce customer {customer_id}")
    
    if not customer_id:
        return {"error": "Customer ID is required"}
    
    # כאן תהיה קריאה אמיתית ל-API של WooCommerce
    return {
        "customer": {
            "id": customer_id,
            "name": "לקוח לדוגמה",
            "email": "customer@example.com",
            "orders_count": 5,
            "total_spent": "750.00"
        }
    }

def get_available_tools():
    """מחזיר רשימה של כלים זמינים ב-MCP"""
    logger.info("Listing available MCP tools")
    return {
        "tools": [
            {
                "name": "list_products",
                "description": "רשימת מוצרים מ-WooCommerce",
                "parameters": []
            },
            {
                "name": "get_product",
                "description": "מידע על מוצר ספציפי",
                "parameters": ["id"]
            },
            {
                "name": "create_product",
                "description": "יצירת מוצר חדש",
                "parameters": ["name", "price", "description"]
            },
            {
                "name": "update_product",
                "description": "עדכון מוצר קיים",
                "parameters": ["id", "name", "price", "description"]
            },
            {
                "name": "delete_product",
                "description": "מחיקת מוצר",
                "parameters": ["id"]
            },
            {
                "name": "list_orders",
                "description": "רשימת הזמנות",
                "parameters": []
            },
            {
                "name": "get_order",
                "description": "מידע על הזמנה ספציפית",
                "parameters": ["id"]
            },
            {
                "name": "get_customer",
                "description": "מידע על לקוח",
                "parameters": ["id"]
            }
        ]
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting MCP server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True', threaded=True) 