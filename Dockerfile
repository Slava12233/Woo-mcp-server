FROM python:3.12-slim

WORKDIR /app

# התקנת כלי הבניה הנדרשים
RUN apt-get update && apt-get install -y build-essential

# התקנת תלויות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד המקור
COPY . .

# חשיפת פורט (פורט ברירת המחדל של MCP הוא 8000)
EXPOSE 8000

# הגדרת משתני סביבה
ENV MCP_PORT=8000
ENV MCP_HOST=0.0.0.0

# הרצת השרת
CMD ["python", "-m", "src.woocommerce_mcp.server"] 