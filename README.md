# 🛒 WooCommerce MCP Server | Python Edition

> *פתרון פשוט ויעיל לחיבור חנויות WooCommerce עם Model Context Protocol*

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

## 📌 מה זה?

שרת Model Context Protocol (MCP) המאפשר אינטגרציה מלאה עם חנויות WooCommerce באמצעות ה-WordPress REST API. הספרייה מספקת כלים מקיפים לניהול כל היבטי המוצרים, הזמנות, לקוחות, משלוח, מיסים, הנחות וקונפיגורציית החנות.

## 🚀 התקנה מהירה

```bash
# שלב 1: שכפל את הרפוזיטורי
git clone https://github.com/yourusername/woocommerce-mcp-server.git
cd woocommerce-mcp-server

# שלב 2: התקן תלויות
pip install -r requirements.txt

# שלב 3: הגדר משתני סביבה (ראה הסבר בהמשך)
```

## ⚙️ קונפיגורציה

יש ליצור קובץ `.env` בתיקיית הבסיס של הפרויקט עם הפרטים הבאים:

```
WORDPRESS_SITE_URL=https://your-wordpress-site.com
WOOCOMMERCE_CONSUMER_KEY=your-woocommerce-consumer-key
WOOCOMMERCE_CONSUMER_SECRET=your-woocommerce-consumer-secret
WORDPRESS_USERNAME=your-wordpress-username
WORDPRESS_PASSWORD=your-wordpress-password
```

### משתני סביבה

| משתנה | תיאור | נדרש |
|--------|-------------|:-----:|
| `WORDPRESS_SITE_URL` | כתובת האתר שלך (WooCommerce הוא פלאגין של WordPress) | ✅ |
| `WOOCOMMERCE_CONSUMER_KEY` | מפתח צרכן WooCommerce REST API | ✅ |
| `WOOCOMMERCE_CONSUMER_SECRET` | סוד צרכן WooCommerce REST API | ✅ |
| `WORDPRESS_USERNAME` | שם משתמש WordPress עם הרשאות מתאימות | ⚠️ * |
| `WORDPRESS_PASSWORD` | סיסמת WordPress לאימות | ⚠️ * |

\* נדרש רק עבור שיטות WordPress API

## 🔐 אפשרויות אימות

### אימות WooCommerce
גישה ל-API של WooCommerce דורשת מפתחות צרכן שניתן ליצור בלוח הבקרה של WordPress תחת WooCommerce → הגדרות → מתקדם → REST API.

### אימות WordPress
עבור שיטות ספציפיות ל-WordPress (כמו ניהול פוסטים), יש לספק:
- אישורי שם משתמש/סיסמה לאימות בסיסי
- ה-REST API של WordPress חייב להיות מופעל באתר שלך

## 🔄 שיטות API

השרת תומך בשיטות API של WordPress ו-WooCommerce. להלן רשימת השיטות הזמינות מקובצות לפי קטגוריה:

### ניהול תוכן WordPress

These methods require WordPress username/password credentials and are independent of the WooCommerce API.

| Method | Description |
|--------|-------------|
| `create_post` | Create a new WordPress post |
| `get_posts` | Retrieve WordPress posts |
| `update_post` | Update an existing WordPress post |
| `get_post_meta` | Get post metadata |
| `update_post_meta` | Update post metadata |
| `create_post_meta` | Create post metadata |
| `delete_post_meta` | Delete post metadata |

### מוצרי WooCommerce

| Method | Description |
|--------|-------------|
| `get_products` | Retrieve a list of products |
| `get_product` | Get a single product by ID |
| `create_product` | Create a new product |
| `update_product` | Update an existing product |
| `delete_product` | Delete a product |
| `get_product_meta` | Get product metadata |
| `create_product_meta` | Create/update product metadata |
| `update_product_meta` | Update product metadata (alias for create) |
| `delete_product_meta` | Delete product metadata |

### קטגוריות מוצרים

| Method | Description |
|--------|-------------|
| `get_product_categories` | Retrieve product categories |
| `get_product_category` | Get a single product category |
| `create_product_category` | Create a new product category |
| `update_product_category` | Update a product category |
| `delete_product_category` | Delete a product category |

### תגיות מוצרים

| Method | Description |
|--------|-------------|
| `get_product_tags` | Retrieve product tags |
| `get_product_tag` | Get a single product tag |
| `create_product_tag` | Create a new product tag |
| `update_product_tag` | Update a product tag |
| `delete_product_tag` | Delete a product tag |

### מאפייני מוצרים

| Method | Description |
|--------|-------------|
| `get_product_attributes` | Retrieve product attributes |
| `get_product_attribute` | Get a single product attribute |
| `create_product_attribute` | Create a new product attribute |
| `update_product_attribute` | Update a product attribute |
| `delete_product_attribute` | Delete a product attribute |
| `get_attribute_terms` | Retrieve attribute terms |
| `get_attribute_term` | Get a single attribute term |
| `create_attribute_term` | Create a new attribute term |
| `update_attribute_term` | Update an attribute term |
| `delete_attribute_term` | Delete an attribute term |

### וריאציות מוצרים

| Method | Description |
|--------|-------------|
| `get_product_variations` | Retrieve product variations |
| `get_product_variation` | Get a single product variation |
| `create_product_variation` | Create a new product variation |
| `update_product_variation` | Update a product variation |
| `delete_product_variation` | Delete a product variation |
| `batch_update_product_variations` | Batch update product variations |

### ביקורות מוצרים

| Method | Description |
|--------|-------------|
| `get_product_reviews` | Retrieve product reviews |
| `get_product_review` | Get a single product review |
| `create_product_review` | Create a new product review |
| `update_product_review` | Update a product review |
| `delete_product_review` | Delete a product review |

### הזמנות WooCommerce

| Method | Description |
|--------|-------------|
| `get_orders` | Retrieve a list of orders |
| `get_order` | Get a single order by ID |
| `create_order` | Create a new order |
| `update_order` | Update an existing order |
| `delete_order` | Delete an order |
| `get_order_meta` | Get order metadata |
| `create_order_meta` | Create/update order metadata |
| `update_order_meta` | Update order metadata (alias for create) |
| `delete_order_meta` | Delete order metadata |

### הערות הזמנה

| Method | Description |
|--------|-------------|
| `get_order_notes` | Retrieve order notes |
| `get_order_note` | Get a single order note |
| `create_order_note` | Create a new order note |
| `delete_order_note` | Delete an order note |

### החזרי הזמנות

| Method | Description |
|--------|-------------|
| `get_order_refunds` | Retrieve order refunds |
| `get_order_refund` | Get a single order refund |
| `create_order_refund` | Create a new order refund |
| `update_order_refund` | Update an order refund |
| `delete_order_refund` | Delete an order refund |

### לקוחות WooCommerce

| Method | Description |
|--------|-------------|
| `get_customers` | Retrieve a list of customers |
| `get_customer` | Get a single customer by ID |
| `create_customer` | Create a new customer |
| `update_customer` | Update an existing customer |
| `delete_customer` | Delete a customer |
| `get_customer_meta` | Get customer metadata |
| `create_customer_meta` | Create/update customer metadata |
| `update_customer_meta` | Update customer metadata (alias for create) |
| `delete_customer_meta` | Delete customer metadata |

### משלוח

| Method | Description |
|--------|-------------|
| `get_shipping_zones` | Retrieve shipping zones |
| `get_shipping_zone` | Get a single shipping zone |
| `create_shipping_zone` | Create a new shipping zone |
| `update_shipping_zone` | Update a shipping zone |
| `delete_shipping_zone` | Delete a shipping zone |
| `get_shipping_methods` | Retrieve shipping methods |
| `get_zone_shipping_methods` | Get shipping methods for a zone |
| `get_zone_shipping_method` | Get a specific shipping method for a zone |
| `create_zone_shipping_method` | Create a new shipping method for a zone |
| `update_zone_shipping_method` | Update a shipping method for a zone |
| `delete_zone_shipping_method` | Delete a shipping method from a zone |
| `get_shipping_zone_locations` | Get locations for a shipping zone |
| `update_shipping_zone_locations` | Update locations for a shipping zone |

### מיסים

| Method | Description |
|--------|-------------|
| `get_tax_classes` | Retrieve tax classes |
| `create_tax_class` | Create a new tax class |
| `delete_tax_class` | Delete a tax class |
| `get_tax_rates` | Retrieve tax rates |
| `get_tax_rate` | Get a single tax rate |
| `create_tax_rate` | Create a new tax rate |
| `update_tax_rate` | Update a tax rate |
| `delete_tax_rate` | Delete a tax rate |
| `batch_update_tax_rates` | Batch update tax rates |

### הנחות/קופונים

| Method | Description |
|--------|-------------|
| `get_coupons` | Retrieve coupons |
| `get_coupon` | Get a single coupon |
| `create_coupon` | Create a new coupon |
| `update_coupon` | Update a coupon |
| `delete_coupon` | Delete a coupon |
| `batch_update_coupons` | Batch update coupons |

### שערי תשלום

| Method | Description |
|--------|-------------|
| `get_payment_gateways` | Retrieve payment gateways |
| `get_payment_gateway` | Get a single payment gateway |
| `update_payment_gateway` | Update a payment gateway |

### דוחות

| Method | Description |
|--------|-------------|
| `get_sales_report` | Retrieve sales reports |
| `get_products_report` | Retrieve products reports |
| `get_customers_report` | Retrieve customers reports |
| `get_stock_report` | Retrieve stock reports |

### הגדרות

| Method | Description |
|--------|-------------|
| `get_settings` | Retrieve all settings |
| `get_setting_option` | Retrieve a specific setting option |
| `update_setting_option` | Update a setting option |
| `batch_update_settings` | Batch update settings |

### מצב מערכת

| Method | Description |
|--------|-------------|
| `get_system_status` | Retrieve system status |
| `get_system_status_tools` | Retrieve system status tools |
| `execute_system_status_tool` | Run a system status tool |

### נתונים

| Method | Description |
|--------|-------------|
| `get_countries` | Retrieve countries data |
| `get_country_states` | Retrieve states/provinces for a country |
| `get_currencies` | Retrieve currencies data |
| `get_currency` | Get details for a specific currency |
| `get_current_currency` | Get the current currency |

## 💻 דוגמאות שימוש

### אתחול שרת MCP

```python
import os
from dotenv import load_dotenv
from woocommerce_mcp import initialize

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# אתחול שרת MCP
mcp = initialize()

# הפעלת השרת
async def main():
    mcp.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### דוגמה לקבלת מוצרים

```python
import asyncio
from woocommerce_mcp.products import get_products

async def list_products():
    # קבלת המוצרים האחרונים
    products = await get_products({
        "per_page": 20, 
        "page": 1,
        "status": "publish"
    })
    
    for product in products:
        print(f"מוצר: {product['name']}, מחיר: {product['price']}")

# הפעלת הפונקציה
asyncio.run(list_products())
```

### דוגמה ליצירת מוצר

```python
import asyncio
from woocommerce_mcp.products import create_product

async def add_new_product():
    product_data = {
        "name": "חולצת פרימיום",
        "type": "simple",
        "regular_price": "99.99",
        "description": "חולצת כותנה נוחה, זמינה במגוון מידות וצבעים.",
        "short_description": "חולצת פרימיום באיכות גבוהה.",
        "categories": [
            {
                "id": 19
            }
        ],
        "images": [
            {
                "src": "http://example.com/wp-content/uploads/2022/06/t-shirt.jpg"
            }
        ]
    }
    
    result = await create_product(product_data)
    print(f"נוצר מוצר חדש עם מזהה: {result['id']}")

# הפעלת הפונקציה
asyncio.run(add_new_product())
```

## 📋 פרמטרים לפונקציות

כל הפונקציות מקבלות את הפרמטרים הספציפיים שלהן לפעולת ה-API, בנוסף לפרמטרים האופציונליים הבאים:

- `site_url`: (אופציונלי אם מוגדר במשתני סביבה) כתובת אתר WordPress
- `consumer_key`: (אופציונלי אם מוגדר במשתני סביבה) מפתח צרכן WooCommerce
- `consumer_secret`: (אופציונלי אם מוגדר במשתני סביבה) סוד צרכן WooCommerce
- עבור שיטות WordPress: `username` ו-`password` (אופציונלי אם מוגדר במשתני סביבה)

## 🔒 הערת אבטחה

לגישה ל-REST API של WooCommerce, עליך ליצור מפתחות API. ניתן ליצור אותם בלוח הבקרה של WordPress תחת WooCommerce → הגדרות → מתקדם → REST API.

## 📦 דרישות מערכת

- Python 3.9 ומעלה
- אתר WordPress עם פלאגין WooCommerce מותקן
- מפתחות REST API של WooCommerce
- חבילות Python: `mcp-server`, `httpx`, `python-dotenv`

## 📄 רישיון

MIT License - ראה קובץ LICENSE לפרטים נוספים 