<a name="hebrew-version"></a>

<div align="center">

# 🛒 WooCommerce MCP Server | Python Edition

</div>

<div dir="rtl">

> *פתרון פשוט ויעיל לחיבור חנויות WooCommerce עם Model Context Protocol*

<div align="right">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

[🇺🇸 English Version](#english-version) | <b>🇮🇱 גרסה עברית</b>

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

<div align="right">

| משתנה | תיאור | נדרש |
|--------|-------------|:-----:|
| `WORDPRESS_SITE_URL` | כתובת האתר שלך (WooCommerce הוא פלאגין של WordPress) | ✅ |
| `WOOCOMMERCE_CONSUMER_KEY` | מפתח צרכן WooCommerce REST API | ✅ |
| `WOOCOMMERCE_CONSUMER_SECRET` | סוד צרכן WooCommerce REST API | ✅ |
| `WORDPRESS_USERNAME` | שם משתמש WordPress עם הרשאות מתאימות | ⚠️ * |
| `WORDPRESS_PASSWORD` | סיסמת WordPress לאימות | ⚠️ * |

</div>

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

שיטות אלה דורשות אישורי שם משתמש/סיסמה של WordPress והן עצמאיות מה-API של WooCommerce.

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `create_post` | יצירת פוסט WordPress חדש |
| `get_posts` | קבלת פוסטים מ-WordPress |
| `update_post` | עדכון פוסט WordPress קיים |
| `get_post_meta` | קבלת מטא-דאטה של פוסט |
| `update_post_meta` | עדכון מטא-דאטה של פוסט |
| `create_post_meta` | יצירת מטא-דאטה של פוסט |
| `delete_post_meta` | מחיקת מטא-דאטה של פוסט |

</div>

### מוצרי WooCommerce

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_products` | קבלת רשימת מוצרים |
| `get_product` | קבלת מוצר בודד לפי מזהה |
| `create_product` | יצירת מוצר חדש |
| `update_product` | עדכון מוצר קיים |
| `delete_product` | מחיקת מוצר |
| `get_product_meta` | קבלת מטא-דאטה של מוצר |
| `create_product_meta` | יצירה/עדכון מטא-דאטה של מוצר |
| `update_product_meta` | עדכון מטא-דאטה של מוצר (כינוי ליצירה) |
| `delete_product_meta` | מחיקת מטא-דאטה של מוצר |

</div>

### קטגוריות מוצרים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_product_categories` | קבלת קטגוריות מוצרים |
| `get_product_category` | קבלת קטגוריית מוצר בודדת |
| `create_product_category` | יצירת קטגוריית מוצר חדשה |
| `update_product_category` | עדכון קטגוריית מוצר |
| `delete_product_category` | מחיקת קטגוריית מוצר |

</div>

### תגיות מוצרים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_product_tags` | קבלת תגיות מוצרים |
| `get_product_tag` | קבלת תגית מוצר בודדת |
| `create_product_tag` | יצירת תגית מוצר חדשה |
| `update_product_tag` | עדכון תגית מוצר |
| `delete_product_tag` | מחיקת תגית מוצר |

</div>

### מאפייני מוצרים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_product_attributes` | קבלת מאפייני מוצרים |
| `get_product_attribute` | קבלת מאפיין מוצר בודד |
| `create_product_attribute` | יצירת מאפיין מוצר חדש |
| `update_product_attribute` | עדכון מאפיין מוצר |
| `delete_product_attribute` | מחיקת מאפיין מוצר |
| `get_attribute_terms` | קבלת מונחי מאפיין |
| `get_attribute_term` | קבלת מונח מאפיין בודד |
| `create_attribute_term` | יצירת מונח מאפיין חדש |
| `update_attribute_term` | עדכון מונח מאפיין |
| `delete_attribute_term` | מחיקת מונח מאפיין |

</div>

### וריאציות מוצרים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_product_variations` | קבלת וריאציות מוצרים |
| `get_product_variation` | קבלת וריאציית מוצר בודדת |
| `create_product_variation` | יצירת וריאציית מוצר חדשה |
| `update_product_variation` | עדכון וריאציית מוצר |
| `delete_product_variation` | מחיקת וריאציית מוצר |
| `batch_update_product_variations` | עדכון אצווה של וריאציות מוצרים |

</div>

### הערות הזמנה

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_order_notes` | קבלת הערות הזמנה |
| `get_order_note` | קבלת הערת הזמנה בודדת |
| `create_order_note` | יצירת הערת הזמנה חדשה |
| `delete_order_note` | מחיקת הערת הזמנה |

</div>

### החזרי הזמנות

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_order_refunds` | קבלת החזרי הזמנות |
| `get_order_refund` | קבלת החזר הזמנה בודד |
| `create_order_refund` | יצירת החזר הזמנה חדש |
| `update_order_refund` | עדכון החזר הזמנה |
| `delete_order_refund` | מחיקת החזר הזמנה |

</div>

### לקוחות WooCommerce

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_customers` | קבלת רשימת לקוחות |
| `get_customer` | קבלת לקוח בודד לפי מזהה |
| `create_customer` | יצירת לקוח חדש |
| `update_customer` | עדכון לקוח קיים |
| `delete_customer` | מחיקת לקוח |
| `get_customer_meta` | קבלת מטא-דאטה של לקוח |
| `create_customer_meta` | יצירה/עדכון מטא-דאטה של לקוח |
| `update_customer_meta` | עדכון מטא-דאטה של לקוח (כינוי ליצירה) |
| `delete_customer_meta` | מחיקת מטא-דאטה של לקוח |

</div>

### משלוח

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_shipping_zones` | קבלת אזורי משלוח |
| `get_shipping_zone` | קבלת אזור משלוח בודד |
| `create_shipping_zone` | יצירת אזור משלוח חדש |
| `update_shipping_zone` | עדכון אזור משלוח |
| `delete_shipping_zone` | מחיקת אזור משלוח |
| `get_shipping_methods` | קבלת שיטות משלוח |
| `get_zone_shipping_methods` | קבלת שיטות משלוח לאזור |
| `get_zone_shipping_method` | קבלת שיטת משלוח ספציפית לאזור |
| `create_zone_shipping_method` | יצירת שיטת משלוח חדשה לאזור |
| `update_zone_shipping_method` | עדכון שיטת משלוח לאזור |
| `delete_zone_shipping_method` | מחיקת שיטת משלוח מאזור |
| `get_shipping_zone_locations` | קבלת מיקומים לאזור משלוח |
| `update_shipping_zone_locations` | עדכון מיקומים לאזור משלוח |

</div>

### מיסים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_tax_classes` | קבלת קטגוריות מס |
| `create_tax_class` | יצירת קטגוריית מס חדשה |
| `delete_tax_class` | מחיקת קטגוריית מס |
| `get_tax_rates` | קבלת שיעורי מס |
| `get_tax_rate` | קבלת שיעור מס בודד |
| `create_tax_rate` | יצירת שיעור מס חדש |
| `update_tax_rate` | עדכון שיעור מס |
| `delete_tax_rate` | מחיקת שיעור מס |
| `batch_update_tax_rates` | עדכון אצווה של שיעורי מס |

</div>

### הנחות/קופונים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_coupons` | קבלת קופונים |
| `get_coupon` | קבלת קופון בודד |
| `create_coupon` | יצירת קופון חדש |
| `update_coupon` | עדכון קופון |
| `delete_coupon` | מחיקת קופון |
| `batch_update_coupons` | עדכון אצווה של קופונים |

</div>

### שערי תשלום

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_payment_gateways` | קבלת שערי תשלום |
| `get_payment_gateway` | קבלת שער תשלום בודד |
| `update_payment_gateway` | עדכון שער תשלום |

</div>

### דוחות

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_sales_report` | קבלת דוחות מכירות |
| `get_products_report` | קבלת דוחות מוצרים |
| `get_customers_report` | קבלת דוחות לקוחות |
| `get_stock_report` | קבלת דוחות מלאי |

</div>

### הגדרות

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_settings` | קבלת כל ההגדרות |
| `get_setting_option` | קבלת אפשרות הגדרה ספציפית |
| `update_setting_option` | עדכון אפשרות הגדרה |
| `batch_update_settings` | עדכון אצווה של הגדרות |

</div>

### מצב מערכת

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_system_status` | קבלת מצב מערכת |
| `get_system_status_tools` | קבלת כלי מצב מערכת |
| `execute_system_status_tool` | הפעלת כלי מצב מערכת |

</div>

### נתונים

<div align="right">

| שיטה | תיאור |
|--------|-------------|
| `get_countries` | קבלת נתוני מדינות |
| `get_country_states` | קבלת מחוזות/מדינות עבור מדינה |
| `get_currencies` | קבלת נתוני מטבעות |
| `get_currency` | קבלת פרטים עבור מטבע ספציפי |
| `get_current_currency` | קבלת המטבע הנוכחי |

</div>

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

</div>

---

<a name="english-version"></a>

<div align="center">

# 🛒 WooCommerce MCP Server | Python Edition

</div>

> *A simple and efficient solution for connecting WooCommerce stores with Model Context Protocol*

<div align="right">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

[<b>🇮🇱 Hebrew Version</b>](#hebrew-version) | 🇺🇸 English Version

## 📌 What is it?

A Model Context Protocol (MCP) server for WooCommerce integration, compatible with WordPress REST API. The library provides comprehensive tools for managing all aspects of products, orders, customers, shipping, taxes, discounts, and store configuration.

## 🚀 Quick Installation

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/woocommerce-mcp-server.git
cd woocommerce-mcp-server

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Configure environment variables (see below)
```

## ⚙️ Configuration

Create a `.env` file in the project root with your credentials:

```
WORDPRESS_SITE_URL=https://your-wordpress-site.com
WOOCOMMERCE_CONSUMER_KEY=your-woocommerce-consumer-key
WOOCOMMERCE_CONSUMER_SECRET=your-woocommerce-consumer-secret
WORDPRESS_USERNAME=your-wordpress-username
WORDPRESS_PASSWORD=your-wordpress-password
```

### Environment Variables

| Variable | Description | Required |
|--------|-------------|:-----:|
| `WORDPRESS_SITE_URL` | Your WordPress site URL (WooCommerce is a WordPress plugin) | ✅ |
| `WOOCOMMERCE_CONSUMER_KEY` | WooCommerce REST API consumer key | ✅ |
| `WOOCOMMERCE_CONSUMER_SECRET` | WooCommerce REST API consumer secret | ✅ |
| `WORDPRESS_USERNAME` | WordPress username with appropriate permissions | ⚠️ * |
| `WORDPRESS_PASSWORD` | WordPress password for authentication | ⚠️ * |

\* Required only for WordPress API methods

## 🔐 Authentication Options

### WooCommerce Authentication
WooCommerce API access requires consumer keys that you can generate in your WordPress dashboard under WooCommerce → Settings → Advanced → REST API.

### WordPress Authentication
For WordPress-specific methods (like managing posts), you need to provide:
- Username/password credentials for basic authentication
- The WordPress REST API must be enabled on your site

## 🔄 API Methods

The server supports both WordPress and WooCommerce API methods. Here's a list of available methods grouped by category:

### WordPress Content Management

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

### WooCommerce Products

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

### Product Categories

| Method | Description |
|--------|-------------|
| `get_product_categories` | Retrieve product categories |
| `get_product_category` | Get a single product category |
| `create_product_category` | Create a new product category |
| `update_product_category` | Update a product category |
| `delete_product_category` | Delete a product category |

### Product Tags

| Method | Description |
|--------|-------------|
| `get_product_tags` | Retrieve product tags |
| `get_product_tag` | Get a single product tag |
| `create_product_tag` | Create a new product tag |
| `update_product_tag` | Update a product tag |
| `delete_product_tag` | Delete a product tag |

### Product Attributes

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

### Product Variations

| Method | Description |
|--------|-------------|
| `get_product_variations` | Retrieve product variations |
| `get_product_variation` | Get a single product variation |
| `create_product_variation` | Create a new product variation |
| `update_product_variation` | Update a product variation |
| `delete_product_variation` | Delete a product variation |
| `batch_update_product_variations` | Batch update product variations |

### Product Reviews

| Method | Description |
|--------|-------------|
| `get_product_reviews` | Retrieve product reviews |
| `get_product_review` | Get a single product review |
| `create_product_review` | Create a new product review |
| `update_product_review` | Update a product review |
| `delete_product_review` | Delete a product review |

### WooCommerce Orders

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

### Order Notes

| Method | Description |
|--------|-------------|
| `get_order_notes` | Retrieve order notes |
| `get_order_note` | Get a single order note |
| `create_order_note` | Create a new order note |
| `delete_order_note` | Delete an order note |

### Order Refunds

| Method | Description |
|--------|-------------|
| `get_order_refunds` | Retrieve order refunds |
| `get_order_refund` | Get a single order refund |
| `create_order_refund` | Create a new order refund |
| `update_order_refund` | Update an order refund |
| `delete_order_refund` | Delete an order refund |

### WooCommerce Customers

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

### Shipping

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

### Taxes

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

### Discounts/Coupons

| Method | Description |
|--------|-------------|
| `get_coupons` | Retrieve coupons |
| `get_coupon` | Get a single coupon |
| `create_coupon` | Create a new coupon |
| `update_coupon` | Update a coupon |
| `delete_coupon` | Delete a coupon |
| `batch_update_coupons` | Batch update coupons |

### Payment Gateways

| Method | Description |
|--------|-------------|
| `get_payment_gateways` | Retrieve payment gateways |
| `get_payment_gateway` | Get a single payment gateway |
| `update_payment_gateway` | Update a payment gateway |

### Reports

| Method | Description |
|--------|-------------|
| `get_sales_report` | Retrieve sales reports |
| `get_products_report` | Retrieve products reports |
| `get_customers_report` | Retrieve customers reports |
| `get_stock_report` | Retrieve stock reports |

### Settings

| Method | Description |
|--------|-------------|
| `get_settings` | Retrieve all settings |
| `get_setting_option` | Retrieve a specific setting option |
| `update_setting_option` | Update a setting option |
| `batch_update_settings` | Batch update settings |

### System Status

| Method | Description |
|--------|-------------|
| `get_system_status` | Retrieve system status |
| `get_system_status_tools` | Retrieve system status tools |
| `execute_system_status_tool` | Run a system status tool |

### Data

| Method | Description |
|--------|-------------|
| `get_countries` | Retrieve countries data |
| `get_country_states` | Retrieve states/provinces for a country |
| `get_currencies` | Retrieve currencies data |
| `get_currency` | Get details for a specific currency |
| `get_current_currency` | Get the current currency |

## 💻 Usage Examples

### Initialize MCP Server

```python
import os
from dotenv import load_dotenv
from woocommerce_mcp import initialize

# Load environment variables from .env
load_dotenv()

# Initialize the MCP server
mcp = initialize()

# Run the server
async def main():
    mcp.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Example for Getting Products

```python
import asyncio
from woocommerce_mcp.products import get_products

async def list_products():
    # Get latest products
    products = await get_products({
        "per_page": 20, 
        "page": 1,
        "status": "publish"
    })
    
    for product in products:
        print(f"Product: {product['name']}, Price: {product['price']}")

# Run the function
asyncio.run(list_products())
```

### Example for Creating a Product

```python
import asyncio
from woocommerce_mcp.products import create_product

async def add_new_product():
    product_data = {
        "name": "Premium T-Shirt",
        "type": "simple",
        "regular_price": "29.99",
        "description": "Comfortable cotton t-shirt, available in various sizes.",
        "short_description": "Premium quality t-shirt.",
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
    print(f"Created new product with ID: {result['id']}")

# Run the function
asyncio.run(add_new_product())
```

## 📋 Function Parameters

All functions accept their specific parameters for the API action, plus the following optional parameters:

- `site_url`: (optional if set in env) WordPress site URL
- `consumer_key`: (optional if set in env) WooCommerce consumer key
- `consumer_secret`: (optional if set in env) WooCommerce consumer secret
- For WordPress methods: `username` and `password` (optional if set in env)

## 🔒 Security Note

For WooCommerce REST API access, you need to generate API keys. You can create them in your WordPress dashboard under WooCommerce → Settings → Advanced → REST API.

## 📦 System Requirements

- Python 3.9 or higher
- WordPress site with WooCommerce plugin installed
- WooCommerce REST API keys
- Python packages: `mcp-server`, `httpx`, `python-dotenv`

## 📄 License

MIT License - See LICENSE file for details 