import asyncio
import os
from playwright.async_api import async_playwright

# Configuration
AMAZON_URL = "https://www.amazon.com"

# STEP 1: Configure your Bright Data Browser API endpoint
# - Get endpoint from: https://brightdata.com/cp/zones
# - Create new Browser API: https://docs.brightdata.com/scraping-automation/scraping-browser/quickstart
# - Websocket format: wss://brd-customer-[id]-zone-[zone]:[password]@[domain]:[port]
BROWSER_WS = os.getenv("BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT", "YOUR_BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT")

# STEP 2: Run `python amazon_product_scraping.py` command in terminal

# Search parameters
SEARCH_TERM = "laptop"  # Change this to search for different products

async def scrape_amazon():
    """
    Main function to run the scraper
    This is the entry point of our script
    """
    print("🚀 Starting Amazon scraper...")
    print(f"🔍 Searching for: {SEARCH_TERM}")

    try:
        async with async_playwright() as p:
            # Step 1: Connect to Bright Data's browser
            print("🌐 Connecting to browser...")
            browser = await p.chromium.connect_over_cdp(BROWSER_WS)
            print("✅ Connected to browser")

            # Step 2: Create a new context and page
            context = await browser.new_context()
            page = await context.new_page()
            
            # Step 3: Go to Amazon
            print("🌐 Opening Amazon...")
            await page.goto(AMAZON_URL, wait_until="domcontentloaded")
            print("✅ Amazon loaded")

            # Step 4: Search for products
            print("🔍 Entering search term...")
            await page.fill('#twotabsearchtextbox', SEARCH_TERM)
            await page.click('#nav-search-submit-button')
            print("✅ Search submitted")

            # Step 5: Wait for results to load
            print("⏳ Waiting for results...")
            await page.wait_for_selector('[data-component-type="s-search-result"]')
            print("✅ Results loaded")

            # Step 6: Extract product information
            print("📊 Extracting product data...")
            
            # Get all product elements
            product_elements = await page.query_selector_all('[data-component-type="s-search-result"]')
            
            products = []
            # Process only first 5 products
            for item in product_elements[:5]:
                # Get product title
                title_element = await item.query_selector('h2')
                title = await title_element.inner_text() if title_element else 'N/A'

                # Get product price
                price_element = await item.query_selector('.a-price .a-offscreen')
                price = await price_element.inner_text() if price_element else 'N/A'

                # Get product rating
                rating_element = await item.query_selector('.a-icon-star-small')
                rating = await rating_element.inner_text() if rating_element else 'N/A'

                products.append({
                    'title': title,
                    'price': price,
                    'rating': rating
                })

            # Step 7: Display results
            print(f"\n📊 AMAZON SEARCH RESULTS for \"{SEARCH_TERM}\"")
            print("=======================")
            
            # Format and display each product in a clean, readable way
            for index, product in enumerate(products):
                print(f"\n#{index + 1} {product['title']}")
                print(f"   💰 Price: {product['price']}")
                print(f"   ⭐ Rating: {product['rating']}")
                print("   " + "-" * 50)
            
            print(f"\n✅ Found {len(products)} products for \"{SEARCH_TERM}\"")

            # Step 8: Close browser
            print("👋 Closing browser...")
            await browser.close()
            print("✅ Browser closed")

    except Exception as error:
        print(f"❌ Error occurred: {error}")

# Run the scraper
if __name__ == "__main__":
    asyncio.run(scrape_amazon())