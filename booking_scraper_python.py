import asyncio
import os
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# Configuration
BOOKING_URL = "https://www.booking.com/"

# STEP 1: Configure your Bright Data Browser API endpoint
# - Get endpoint from: https://brightdata.com/cp/zones
# - Create new Browser API: https://docs.brightdata.com/scraping-automation/scraping-browser/quickstart
# - Websocket format: wss://brd-customer-[id]-zone-[zone]:[password]@[domain]:[port]
BROWSER_WS = os.getenv("BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT", "YOUR_BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT")

# STEP 2: Run `python booking_hotel_scraping.py` command in terminal

# Search parameters
SEARCH_LOCATION = "New York"
CHECK_IN_DAYS_FROM_NOW = 1   # Check-in tomorrow
CHECK_OUT_DAYS_FROM_NOW = 2  # Check-out day after tomorrow

def add_days(date, days):
    """Helper function to add days to a date"""
    return date + timedelta(days=days)

def format_date(date):
    """Helper function to format date for Booking.com"""
    return date.strftime('%Y-%m-%d')

# Calculate check-in and check-out dates
today = datetime.now()
check_in_date = format_date(add_days(today, CHECK_IN_DAYS_FROM_NOW))
check_out_date = format_date(add_days(today, CHECK_OUT_DAYS_FROM_NOW))

async def search_hotels():
    """Main function to run the hotel search"""
    print("🔍 Starting hotel search process...")
    print(f"📍 Searching for hotels in: {SEARCH_LOCATION}")
    print(f"📅 Check-in date: {check_in_date}")
    print(f"📅 Check-out date: {check_out_date}")
    
    try:
        async with async_playwright() as p:
            # Connect to browser
            print("🌐 Connecting to browser...")
            browser = await p.chromium.connect_over_cdp(BROWSER_WS)
            print("✅ Successfully connected to browser")
            
            # Create a new context and page
            context = await browser.new_context()
            page = await context.new_page()
            
            # Open Booking.com
            print("🌐 Opening Booking.com...")
            await page.goto(BOOKING_URL, wait_until="domcontentloaded", timeout=60000)
            print("✅ Successfully loaded Booking.com")
            
            # Handle popup if it appears
            await handle_popup(page)
            
            # Fill search form and submit
            print("📝 Filling search form...")
            await fill_search_form(page)
            print("✅ Search form submitted successfully")
            
            # Get and display results
            print("🔍 Searching for available hotels...")
            results = await get_hotel_results(page)
            
            # Display results in a table format
            print("\n📊 Search Results:")
            print("==================")
            
            # Display results
            for index, hotel in enumerate(results, 1):
                print(f"\n#{index}")
                print(f"Hotel Name: {hotel['name']}")
                print(f"Price: {hotel['price']}")
                print(f"Rating: {hotel['rating']}")
                print("-" * 50)
            
            print(f"\n✅ Found {len(results)} hotels")
            
            # Close browser
            print("👋 Closing browser...")
            await browser.close()
            print("✅ Browser closed successfully")
            
    except Exception as error:
        print(f"❌ Error occurred: {error}")

async def handle_popup(page):
    """Handle the sign-in popup if it appears"""
    try:
        print("⚠️ Checking for popup...")
        close_button = await page.wait_for_selector('[aria-label="Dismiss sign-in info."]', timeout=25000)
        await close_button.click()
        print("✅ Popup closed successfully")
    except Exception as e:
        print("ℹ️ No popup appeared - continuing with search")

async def fill_search_form(page):
    """Fill and submit the search form"""
    # Fill location
    print("📍 Entering search location...")
    await page.wait_for_selector('[data-testid="destination-container"] input')
    await page.fill('[data-testid="destination-container"] input', SEARCH_LOCATION)
    print("✅ Location entered successfully")
    
    # Select dates
    print("📅 Selecting dates...")
    await page.click('[data-testid="searchbox-dates-container"]')
    await page.wait_for_selector('[data-testid="searchbox-datepicker-calendar"]')
    await page.click(f'[data-date="{check_in_date}"]')
    await page.click(f'[data-date="{check_out_date}"]')
    print("✅ Dates selected successfully")
    
    # Submit search
    print("🔍 Submitting search...")
    
    # Wait for navigation after clicking submit
    async with page.expect_navigation(wait_until='domcontentloaded'):
        await page.click('button[type="submit"]')
    
    print("✅ Search submitted successfully")

async def get_hotel_results(page):
    """Extract hotel information from search results"""
    print("🏨 Extracting hotel information...")
    
    # Get all hotel card elements
    hotel_cards = await page.query_selector_all('[data-testid="property-card"]')
    
    results = []
    for card in hotel_cards:
        # Extract hotel name
        name_element = await card.query_selector('[data-testid="title"]')
        name = await name_element.inner_text() if name_element else 'N/A'
        
        # Extract price
        price_element = await card.query_selector('[data-testid="price-and-discounted-price"]')
        price = await price_element.inner_text() if price_element else 'N/A'
        
        # Extract rating
        rating_element = await card.query_selector('[data-testid="review-score"]')
        rating = await rating_element.inner_text() if rating_element else 'N/A'
        
        results.append({
            'name': name,
            'price': price,
            'rating': rating
        })
    
    return results

# Start the search
if __name__ == "__main__":
    asyncio.run(search_hotels())