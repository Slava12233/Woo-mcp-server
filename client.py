import asyncio
from mcp.client import ClientSession
from mcp.client.sse import sse_client
import logging

# הגדרת לוגר
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# כתובת השרת המרוחק שלך (שנה לכתובת האמיתית שלך מ-Railway)
SERVER_URL = "https://your-railway-service-url.railway.app"

async def run_mcp_client():
    """הדגמת שימוש בלקוח MCP מרוחק"""
    
    logger.info(f"Connecting to MCP server at {SERVER_URL}")
    
    # יצירת חיבור לשרת המרוחק
    async with sse_client(SERVER_URL) as (read, write):
        # יצירת סשן
        async with ClientSession(read, write) as session:
            # אתחול
            await session.initialize()
            logger.info("MCP session initialized")
            
            # הצגת הכלים הזמינים
            tools = await session.list_tools()
            logger.info(f"Available tools: {[tool.name for tool in tools]}")
            
            # הצגת הפרומפטים הזמינים
            prompts = await session.list_prompts()
            logger.info(f"Available prompts: {[prompt.name for prompt in prompts]}")
            
            # הצגת המשאבים הזמינים
            resources = await session.list_resources()
            logger.info(f"Available resources: {[resource.uri_template for resource in resources]}")
            
            # קריאה למשאב
            help_content, mime_type = await session.read_resource("woo://help")
            logger.info(f"Help content: {help_content[:100]}...")
            
            # קריאה לכלים
            products_result = await session.call_tool("list_products")
            logger.info(f"Products: {products_result}")
            
            # קבלת מידע על מוצר ספציפי
            product_result = await session.call_tool("get_product", {"id": 1})
            logger.info(f"Product info: {product_result}")
            
            # שימוש בפרומפט
            prompt_result = await session.get_prompt("product_search", {"search_term": "מוצר לדוגמה"})
            logger.info(f"Prompt template: {prompt_result}")

if __name__ == "__main__":
    asyncio.run(run_mcp_client()) 