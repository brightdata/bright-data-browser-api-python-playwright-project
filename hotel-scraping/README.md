# Bright Data Hotel Search Scraper with Playwright

This project demonstrates how to use Bright Data's Browser API with Playwright to search for hotels on Booking.com. It provides a practical example of web scraping with automated browser control using Playwright.

<a href="https://codesandbox.io/p/devbox/github/brightdata/bright-data-browser-api-python-playwright-project?file=%2Findex.py" target="_blank" rel="noopener">Open in CodeSandbox</a>, sign in with GitHub account, then fork the repository to begin making changes.

### Getting Started

1. Replace `YOUR_BRIGHT_DATA_SCRAPING_BROWSER_ENDPOINT` with your actual Bright Data Browser API webSocket endpoint in `booking-hotel-scraping.js`
2. Run `python booking-hotel-scraping.js` to start scraping


## 💻 Usage

1. Modify search parameters in `booking-hotel-scraping.js`:
   ```javascript
   const SEARCH_LOCATION = "New York";  // Change to your desired location
   const CHECK_IN_DAYS_FROM_NOW = 1;    // Adjust check-in date
   const CHECK_OUT_DAYS_FROM_NOW = 2;   // Adjust check-out date
   ```

2. Run the script:
   ```bash
   python booking-hotel-scraping.js
   ```

## 📊 Example Output

```
📊 Search Results:
==================
┌─────────┬─────┬────────────────────┬──────────┬─────────┐
│ (index) │  #  │     Hotel Name     │  Price   │ Rating  │
├─────────┼─────┼────────────────────┼──────────┼─────────┤
│    0    │  1  │ Hotel Name 1       │ $100     │ 8.5     │
│    1    │  2  │ Hotel Name 2       │ $150     │ 9.0     │
│    2    │  3  │ Hotel Name 3       │ $200     │ 8.8     │
└─────────┴─────┴────────────────────┴──────────┴─────────┘
```