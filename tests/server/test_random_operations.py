"""
סקריפט המבצע 10 פעולות שונות בחנות WooCommerce בצורה רנדומלית
"""

import os
import asyncio
import random
import string
import httpx
from dotenv import load_dotenv
from datetime import datetime, timedelta

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# קבלת פרטי חיבור
SITE_URL = os.environ.get("WORDPRESS_SITE_URL")
CONSUMER_KEY = os.environ.get("WOOCOMMERCE_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("WOOCOMMERCE_CONSUMER_SECRET")

# פונקציה ליצירת לקוח WooCommerce
async def create_wc_client():
    """יצירת לקוח HTTP לגישה ל-API של WooCommerce"""
    if not SITE_URL:
        raise ValueError("WORDPRESS_SITE_URL לא הוגדר")
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        raise ValueError("פרטי הזדהות WooCommerce לא הוגדרו")
    
    base_url = f"{SITE_URL}/wp-json/wc/v3"
    return httpx.AsyncClient(
        base_url=base_url,
        params={"consumer_key": CONSUMER_KEY, "consumer_secret": CONSUMER_SECRET},
        headers={"Content-Type": "application/json"},
        timeout=30.0
    )

# פונקציות לביצוע פעולות שונות

async def operation_1_create_coupon():
    """פעולה 1: יצירת קופון חדש"""
    print("\n--- מבצע פעולה 1: יצירת קופון חדש ---")
    
    # יצירת קוד קופון רנדומלי
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # נתוני הקופון
    coupon_data = {
        "code": f"TEST{code}",
        "discount_type": "percent",
        "amount": str(random.randint(5, 30)),
        "individual_use": True,
        "exclude_sale_items": True,
        "minimum_amount": "50.00",
        "usage_limit": 1,
        "usage_limit_per_user": 1
    }
    
    async with await create_wc_client() as client:
        response = await client.post("/coupons", json=coupon_data)
        
        if response.status_code >= 400:
            print(f"שגיאה ביצירת קופון: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ קופון נוצר בהצלחה!")
        print(f"מזהה: {result['id']}")
        print(f"קוד: {result['code']}")
        print(f"הנחה: {result['amount']}%")
        return True

async def operation_2_update_product_name():
    """פעולה 2: עדכון שם של מוצר קיים"""
    print("\n--- מבצע פעולה 2: עדכון שם של מוצר ---")
    
    # קבלת רשימת מוצרים
    async with await create_wc_client() as client:
        response = await client.get("/products", params={"per_page": 10})
        
        if response.status_code >= 400 or not response.json():
            print(f"שגיאה בקבלת מוצרים: {response.status_code}")
            return False
        
        products = response.json()
        if not products:
            print("לא נמצאו מוצרים לעדכון")
            return False
        
        # בחירת מוצר רנדומלי
        product = random.choice(products)
        product_id = product["id"]
        old_name = product["name"]
        
        # יצירת שם חדש
        new_name = f"{old_name} - מעודכן {datetime.now().strftime('%H:%M:%S')}"
        
        # עדכון שם המוצר
        update_data = {
            "name": new_name
        }
        
        response = await client.put(f"/products/{product_id}", json=update_data)
        
        if response.status_code >= 400:
            print(f"שגיאה בעדכון מוצר: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ שם המוצר עודכן בהצלחה!")
        print(f"מזהה מוצר: {result['id']}")
        print(f"שם ישן: {old_name}")
        print(f"שם חדש: {result['name']}")
        return True

async def operation_3_create_product_category():
    """פעולה 3: יצירת קטגוריית מוצר חדשה"""
    print("\n--- מבצע פעולה 3: יצירת קטגוריית מוצר חדשה ---")
    
    # יצירת שם קטגוריה רנדומלי
    category_name = f"קטגוריה {random.randint(100, 999)}"
    
    # נתוני הקטגוריה
    category_data = {
        "name": category_name,
        "description": f"קטגוריה לבדיקה שנוצרה ב-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    async with await create_wc_client() as client:
        response = await client.post("/products/categories", json=category_data)
        
        if response.status_code >= 400:
            print(f"שגיאה ביצירת קטגוריה: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ קטגוריה נוצרה בהצלחה!")
        print(f"מזהה: {result['id']}")
        print(f"שם: {result['name']}")
        print(f"תיאור: {result['description']}")
        return True

async def operation_4_get_system_status():
    """פעולה 4: קבלת סטטוס מערכת"""
    print("\n--- מבצע פעולה 4: קבלת סטטוס מערכת ---")
    
    async with await create_wc_client() as client:
        response = await client.get("/system_status")
        
        if response.status_code >= 400:
            print(f"שגיאה בקבלת סטטוס מערכת: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ סטטוס מערכת התקבל בהצלחה!")
        print(f"גרסת WordPress: {result.get('environment', {}).get('wordpress_version', 'לא ידוע')}")
        print(f"גרסת WooCommerce: {result.get('environment', {}).get('version', 'לא ידוע')}")
        print(f"גרסת PHP: {result.get('environment', {}).get('php_version', 'לא ידוע')}")
        print(f"מסד נתונים: {result.get('database', {}).get('wc_database_version', 'לא ידוע')}")
        return True

async def operation_5_create_product_tag():
    """פעולה 5: יצירת תגית מוצר חדשה"""
    print("\n--- מבצע פעולה 5: יצירת תגית מוצר חדשה ---")
    
    # יצירת שם תגית רנדומלי
    tag_name = f"תגית {random.randint(100, 999)}"
    
    # נתוני התגית
    tag_data = {
        "name": tag_name,
        "description": f"תגית לבדיקה שנוצרה ב-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    async with await create_wc_client() as client:
        response = await client.post("/products/tags", json=tag_data)
        
        if response.status_code >= 400:
            print(f"שגיאה ביצירת תגית: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ תגית נוצרה בהצלחה!")
        print(f"מזהה: {result['id']}")
        print(f"שם: {result['name']}")
        print(f"תיאור: {result['description']}")
        return True

async def operation_6_create_product():
    """פעולה 6: יצירת מוצר חדש"""
    print("\n--- מבצע פעולה 6: יצירת מוצר חדש ---")
    
    # נתוני המוצר
    product_data = {
        "name": f"מוצר בדיקה {random.randint(1000, 9999)}",
        "type": "simple",
        "regular_price": str(random.randint(50, 500)) + ".99",
        "description": f"מוצר לבדיקה שנוצר ב-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "short_description": "מוצר לבדיקה",
        "status": "publish"
    }
    
    async with await create_wc_client() as client:
        response = await client.post("/products", json=product_data)
        
        if response.status_code >= 400:
            print(f"שגיאה ביצירת מוצר: {response.status_code} - {response.text}")
            return False
        
        result = response.json()
        print(f"✅ מוצר נוצר בהצלחה!")
        print(f"מזהה: {result['id']}")
        print(f"שם: {result['name']}")
        print(f"מחיר: {result['regular_price']}")
        print(f"קישור: {result['permalink']}")
        return True

async def operation_7_get_shop_settings():
    """פעולה 7: קבלת הגדרות החנות"""
    print("\n--- מבצע פעולה 7: קבלת הגדרות החנות ---")
    
    async with await create_wc_client() as client:
        response = await client.get("/settings/general")
        
        if response.status_code >= 400:
            print(f"שגיאה בקבלת הגדרות החנות: {response.status_code} - {response.text}")
            return False
        
        settings = response.json()
        print(f"✅ הגדרות החנות התקבלו בהצלחה!")
        
        # הצגת הגדרות מעניינות
        for setting in settings:
            if setting.get('id') in ['woocommerce_currency', 'woocommerce_currency_pos', 'woocommerce_price_thousand_sep', 'woocommerce_price_decimal_sep']:
                print(f"{setting.get('label', 'לא ידוע')}: {setting.get('value', 'לא מוגדר')}")
        
        return True

async def operation_8_check_payment_gateways():
    """פעולה 8: בדיקת שערי תשלום זמינים"""
    print("\n--- מבצע פעולה 8: בדיקת שערי תשלום זמינים ---")
    
    async with await create_wc_client() as client:
        response = await client.get("/payment_gateways")
        
        if response.status_code >= 400:
            print(f"שגיאה בקבלת שערי תשלום: {response.status_code} - {response.text}")
            return False
        
        gateways = response.json()
        print(f"✅ רשימת שערי תשלום התקבלה בהצלחה!")
        print(f"נמצאו {len(gateways)} שערי תשלום:")
        
        for gateway in gateways:
            status = "פעיל" if gateway.get('enabled') else "לא פעיל"
            print(f"- {gateway.get('title', 'לא ידוע')} ({gateway.get('id', 'לא ידוע')}): {status}")
        
        return True

async def operation_9_check_shipping_zones():
    """פעולה 9: בדיקת אזורי משלוח"""
    print("\n--- מבצע פעולה 9: בדיקת אזורי משלוח ---")
    
    async with await create_wc_client() as client:
        response = await client.get("/shipping/zones")
        
        if response.status_code >= 400:
            print(f"שגיאה בקבלת אזורי משלוח: {response.status_code} - {response.text}")
            return False
        
        zones = response.json()
        print(f"✅ רשימת אזורי משלוח התקבלה בהצלחה!")
        
        if not zones:
            print("לא נמצאו אזורי משלוח מוגדרים")
            return True
        
        print(f"נמצאו {len(zones)} אזורי משלוח:")
        for zone in zones:
            print(f"- {zone.get('name', 'לא ידוע')} (מזהה: {zone.get('id', 'לא ידוע')})")
            
            # בדיקת שיטות משלוח לאזור
            zone_id = zone.get('id')
            if zone_id:
                methods_response = await client.get(f"/shipping/zones/{zone_id}/methods")
                if methods_response.status_code < 400:
                    methods = methods_response.json()
                    if methods:
                        print(f"  שיטות משלוח באזור זה:")
                        for method in methods:
                            print(f"  - {method.get('title', 'לא ידוע')} ({method.get('method_id', 'לא ידוע')})")
                    else:
                        print("  אין שיטות משלוח מוגדרות לאזור זה")
        
        return True

async def operation_10_get_sales_report():
    """פעולה 10: קבלת דוח מכירות"""
    print("\n--- מבצע פעולה 10: קבלת דוח מכירות ---")
    
    # חישוב תאריכים לחודש אחרון
    today = datetime.now()
    month_ago = today - timedelta(days=30)
    
    params = {
        "date_min": month_ago.strftime("%Y-%m-%d"),
        "date_max": today.strftime("%Y-%m-%d")
    }
    
    async with await create_wc_client() as client:
        response = await client.get("/reports/sales", params=params)
        
        if response.status_code >= 400:
            print(f"שגיאה בקבלת דוח מכירות: {response.status_code} - {response.text}")
            return False
        
        report = response.json()
        
        if not report:
            print("לא התקבלו נתוני מכירות")
            return True
        
        print(f"✅ דוח מכירות התקבל בהצלחה!")
        print(f"תקופה: {month_ago.strftime('%Y-%m-%d')} עד {today.strftime('%Y-%m-%d')}")
        
        if isinstance(report, list) and len(report) > 0:
            report = report[0]  # הדוח הראשון ברשימה
        
        total_sales = report.get('total_sales', '0')
        net_sales = report.get('net_sales', '0')
        average_sales = report.get('average_sales', '0')
        total_orders = report.get('total_orders', 0)
        total_items = report.get('total_items', 0)
        
        print(f"סה\"כ מכירות: {total_sales}")
        print(f"מכירות נטו: {net_sales}")
        print(f"ממוצע מכירות: {average_sales}")
        print(f"סה\"כ הזמנות: {total_orders}")
        print(f"סה\"כ פריטים: {total_items}")
        
        return True

async def main():
    """פונקציה ראשית להרצת 10 פעולות רנדומליות"""
    print(f"=== מתחיל בדיקת פעולות רנדומליות בחנות: {SITE_URL} ===\n")
    
    # רשימת כל הפעולות
    operations = [
        (operation_1_create_coupon, "יצירת קופון"),
        (operation_2_update_product_name, "עדכון שם מוצר"),
        (operation_3_create_product_category, "יצירת קטגוריית מוצר"),
        (operation_4_get_system_status, "קבלת סטטוס מערכת"),
        (operation_5_create_product_tag, "יצירת תגית מוצר"),
        (operation_6_create_product, "יצירת מוצר חדש"),
        (operation_7_get_shop_settings, "קבלת הגדרות חנות"),
        (operation_8_check_payment_gateways, "בדיקת שערי תשלום"),
        (operation_9_check_shipping_zones, "בדיקת אזורי משלוח"),
        (operation_10_get_sales_report, "קבלת דוח מכירות")
    ]
    
    # ערבוב רנדומלי של הפעולות
    random.shuffle(operations)
    
    # מעקב אחרי הצלחה/כישלון
    successful = 0
    failed = 0
    
    # הרצת כל הפעולות בסדר רנדומלי
    for i, (op_func, op_name) in enumerate(operations, 1):
        print(f"\n>>> פעולה {i}/10: {op_name}")
        try:
            result = await op_func()
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ שגיאה כללית בביצוע הפעולה: {e}")
            failed += 1
    
    # סיכום
    print(f"\n=== סיכום בדיקות ===")
    print(f"סה\"כ פעולות: 10")
    print(f"הצליחו: {successful}")
    print(f"נכשלו: {failed}")
    print(f"אחוז הצלחה: {successful * 10}%")


if __name__ == "__main__":
    asyncio.run(main()) 