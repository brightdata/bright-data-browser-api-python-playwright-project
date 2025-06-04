#!/usr/bin/env python3
import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BROWSER_WEBSOCKET_ENDPOINT = os.getenv('BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT')
TARGET_URL = os.getenv('TARGET_URL', 'https://example.com')

async def scrape_with_bright_data(url=TARGET_URL):
    """
    Main scraping function using Bright Data Browser API with Playwright
    """
    if not BROWSER_WEBSOCKET_ENDPOINT or BROWSER_WEBSOCKET_ENDPOINT == "YOUR_BRIGHT_DATA_BROWSER_API_WEBSOCKET_ENDPOINT":
        raise Exception('Please provide valid Bright Data WebSocket endpoint in .env file')
    
    async with async_playwright() as p:
        print("Connecting to Bright Data Browser API...")
        
        try:
            # Connect to the remote browser using the WebSocket endpoint
            browser = await p.chromium.connect_over_cdp(BROWSER_WEBSOCKET_ENDPOINT)
            
            print(f"Connected! Navigating to {url}...")
            
            # Create a new page
            page = await browser.new_page()
            
            # Navigate to the target URL with timeout
            await page.goto(url, timeout=120000)  # 2 minutes timeout
            
            print("Page loaded! Extracting data...")
            
            # Example: Extract page title
            title = await page.title()
            print(f"Page Title: {title}")
            
            # Example: Extract page content
            content = await page.content()
            print(f"Page HTML length: {len(content)} characters")
            
            # Example: Extract specific elements
            # Uncomment and modify based on your needs
            # headings = await page.query_selector_all('h1, h2, h3')
            # for heading in headings:
            #     text = await heading.text_content()
            #     print(f"Heading: {text}")
            
            # Example: Take a screenshot
            await page.screenshot(path='screenshot.png')
            print("Screenshot saved as screenshot.png")
            
            print("Scraping completed successfully!")
            return {
                'title': title,
                'content_length': len(content),
                'url': url
            }
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            raise
        finally:
            print("Closing browser connection...")
            await browser.close()

async def main():
    """Main execution function"""
    try:
        result = await scrape_with_bright_data()
        print(f"Scraping result: {result}")
    except Exception as e:
        print(f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 
