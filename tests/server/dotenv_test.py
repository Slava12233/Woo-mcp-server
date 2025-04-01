import os
from dotenv import load_dotenv

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# הדפסת משתני הסביבה שנטענו
print("משתני סביבה שנטענו מקובץ .env:")
print(f"WORDPRESS_SITE_URL: {os.environ.get('WORDPRESS_SITE_URL', 'לא נמצא')}")
print(f"WORDPRESS_USERNAME: {os.environ.get('WORDPRESS_USERNAME', 'לא נמצא')}")
print(f"WORDPRESS_PASSWORD: {os.environ.get('WORDPRESS_PASSWORD', 'לא נמצא')}")
print(f"WOOCOMMERCE_CONSUMER_KEY: {os.environ.get('WOOCOMMERCE_CONSUMER_KEY', 'לא נמצא')}")
print(f"WOOCOMMERCE_CONSUMER_SECRET: {os.environ.get('WOOCOMMERCE_CONSUMER_SECRET', 'לא נמצא')}") 