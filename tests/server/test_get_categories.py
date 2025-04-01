"""
סקריפט בדיקה לקבלת רשימת קטגוריות מוצרים באמצעות שרת MCP של WooCommerce
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# הוספת src לנתיב החיפוש
sys.path.insert(0, os.path.abspath("src"))

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# במקום לייבא את get_product_categories ישירות, אנחנו משתמשים ב-mcp
from woocommerce_mcp.server import initialize


async def main():
    """קבלת רשימת קטגוריות מוצרים מחנות WooCommerce"""
    print("מקבל רשימת קטגוריות מוצרים מהחנות...")
    
    try:
        # אתחול ה-MCP
        mcp = initialize()
        
        # קבלת רשימת הקטגוריות באמצעות ה-MCP client
        categories = await mcp.get_product_categories(per_page=50)
        
        if categories:
            print(f"\nנמצאו {len(categories)} קטגוריות:")
            for category in categories:
                print(f"מזהה: {category['id']} | שם: {category['name']} | כמות מוצרים: {category['count']}")
        else:
            print("לא נמצאו קטגוריות בחנות.")
    except Exception as e:
        print(f"שגיאה בקבלת קטגוריות: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 