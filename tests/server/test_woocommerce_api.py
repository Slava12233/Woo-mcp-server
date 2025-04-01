"""
סקריפט בדיקה לגישה ישירה ל-API של WooCommerce
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

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
        headers={"Content-Type": "application/json"}
    )

async def get_categories():
    """קבלת רשימת קטגוריות מוצרים"""
    async with await create_wc_client() as client:
        response = await client.get("/products/categories", params={"per_page": 50})
        if response.status_code >= 400:
            print(f"שגיאה בקבלת קטגוריות: {response.status_code} - {response.text}")
            return []
        
        return response.json()

async def create_product(product_data):
    """יצירת מוצר חדש"""
    async with await create_wc_client() as client:
        response = await client.post("/products", json=product_data)
        if response.status_code >= 400:
            print(f"שגיאה ביצירת מוצר: {response.status_code} - {response.text}")
            return None
        
        return response.json()

async def main():
    """פונקציה ראשית לבדיקת גישה ל-API של WooCommerce"""
    print(f"מתחבר לאתר: {SITE_URL}")
    
    # בדיקת קבלת קטגוריות
    print("\nמקבל רשימת קטגוריות...")
    categories = await get_categories()
    if categories:
        print(f"נמצאו {len(categories)} קטגוריות:")
        for category in categories:
            print(f"מזהה: {category['id']} | שם: {category['name']} | כמות מוצרים: {category['count']}")
    else:
        print("לא נמצאו קטגוריות.")
    
    # בדיקת יצירת מוצר
    print("\nיוצר מוצר חדש...")
    
    # יצירת מוצר לדוגמה
    # אם יש קטגוריות, נשתמש בראשונה מהן
    category_id = categories[0]["id"] if categories else None
    
    product_data = {
        "name": "מוצר בדיקה מקוד Python",
        "type": "simple",
        "regular_price": "99.99",
        "description": "זהו מוצר שנוצר ישירות דרך ה-API של WooCommerce לבדיקת חיבור",
        "short_description": "מוצר לבדיקת חיבור",
        "status": "publish"
    }
    
    if category_id:
        product_data["categories"] = [{"id": category_id}]
    
    product = await create_product(product_data)
    
    if product:
        print("המוצר נוצר בהצלחה!")
        print(f"מזהה: {product['id']}")
        print(f"שם: {product['name']}")
        print(f"מחיר: {product['regular_price']}")
        print(f"קישור: {product['permalink']}")
    else:
        print("לא הצלחנו ליצור את המוצר.")


if __name__ == "__main__":
    asyncio.run(main()) 