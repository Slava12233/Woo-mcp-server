"""
סקריפט בדיקה לקבלת רשימת קטגוריות מוצרים באמצעות שרת MCP של WooCommerce
"""

import os
import sys
import asyncio
import requests
from dotenv import load_dotenv

# הוספת src לנתיב החיפוש
sys.path.insert(0, os.path.abspath("src"))

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# נשתמש ב-requests במקום ב-MCP ישירות
async def main():
    """קבלת רשימת קטגוריות מוצרים מחנות WooCommerce"""
    print("מקבל רשימת קטגוריות מוצרים מהחנות...")
    
    try:
        # קריאה ישירה ל-API של WooCommerce במקום דרך MCP
        site_url = os.environ.get("WORDPRESS_SITE_URL")
        consumer_key = os.environ.get("WOOCOMMERCE_CONSUMER_KEY")
        consumer_secret = os.environ.get("WOOCOMMERCE_CONSUMER_SECRET")
        
        if not all([site_url, consumer_key, consumer_secret]):
            print("נא להגדיר את משתני הסביבה הדרושים")
            return
        
        print(f"מתחבר ל-API של {site_url}...")
        
        # בניית הכתובת עם פרמטרי האימות
        url = f"{site_url}/wp-json/wc/v3/products/categories"
        params = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "per_page": 50
        }
        
        # שליחת הבקשה
        response = requests.get(url, params=params)
        
        # בדיקת התגובה
        if response.status_code == 200:
            categories = response.json()
            print(f"\nנמצאו {len(categories)} קטגוריות:")
            for category in categories:
                print(f"מזהה: {category['id']} | שם: {category['name']} | כמות מוצרים: {category['count']}")
        else:
            print(f"שגיאה בקבלת קטגוריות: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"שגיאה בקבלת קטגוריות: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 