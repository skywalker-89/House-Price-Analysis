import asyncio
import random
import json
from playwright.async_api import async_playwright

BASE_URL = "https://www.zoopla.co.uk/for-sale/property/london/?pn={}"

# List of rotating headers (user-agent strings)
HEADERS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
]


async def run(pw):
    print("Launching browser in headless mode...")
    browser = await pw.chromium.launch(headless=False)  # Run in headless mode

    # List to store the house data
    house_data = []

    try:
        house_id = 1
        page_number = 1

        while house_id <= 100:
            # Rotate headers by choosing a random user agent
            user_agent = random.choice(HEADERS)
            print(f"Using User-Agent: {user_agent}")
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            # Construct the URL for the current page
            current_url = BASE_URL.format(page_number)
            print(f"Navigating to {current_url}")

            # Navigate to the current page
            await page.goto(current_url, timeout=60000)

            # Check for CAPTCHA box
            try:
                await page.wait_for_selector(
                    'div[id="content"][aria-live="polite"]', timeout=3000
                )
                print("CAPTCHA detected. Please solve it manually in the browser.")
                input("Solve the CAPTCHA and press Enter to continue...")
            except Exception as e:
                print("No CAPTCHA detected or error occurred:", e)

            # Handle pop-ups or dialogs if present
            try:
                await page.wait_for_selector(
                    'button[aria-label="Close dialog"]', timeout=3000
                )
                await page.click('button[aria-label="Close dialog"]')
                print("Closed the pop-up dialog.")
            except Exception:
                print("No pop-up dialog found.")

            # Click the "Accept Cookies" button if it appears
            try:
                await page.wait_for_selector(
                    "#onetrust-accept-btn-handler", timeout=5000
                )
                await page.click("#onetrust-accept-btn-handler")
                print("Clicked 'Accept Cookies'")
            except Exception:
                print("No 'Accept Cookies' button found or failed to click.")

            # Wait for the listings container to load
            await page.wait_for_selector(
                'div.dkr2t81[data-testid="regular-listings"]', timeout=20000
            )

            # Select the container with listings
            listings_container = await page.query_selector(
                'div.dkr2t81[data-testid="regular-listings"]'
            )

            listings = await listings_container.query_selector_all(
                'div[id^="listing_"]'
            )

            # Extract details for each listing within the container
            for listing in listings:
                if house_id > 100:
                    break

                # Extract link
                link_element = await listing.query_selector("a._1lw0o5c1")
                link = (
                    await link_element.get_attribute("href") if link_element else None
                )
                full_url = BASE_URL.split("/for-sale")[0] + link if link else "N/A"

                # Extract address
                address_element = await listing.query_selector(
                    "address.m6hnz62._194zg6t9"
                )
                address = (
                    await address_element.inner_text() if address_element else "N/A"
                )

                # Extract tenure
                tenure_element = await listing.query_selector(
                    "div.jc64990.jc64994._194zg6t9 div._14bi3x30"
                )
                tenure = await tenure_element.inner_text() if tenure_element else "N/A"

                # Extract beds, baths, and receptions
                details_elements = await listing.query_selector_all(
                    "p._1wickv3._194zg6t9 span._1wickv4"
                )
                beds = (
                    await details_elements[0].inner_text()
                    if len(details_elements) > 0
                    else "N/A"
                )
                baths = (
                    await details_elements[1].inner_text()
                    if len(details_elements) > 1
                    else "N/A"
                )
                receptions = (
                    await details_elements[2].inner_text()
                    if len(details_elements) > 2
                    else "N/A"
                )

                # Extract price
                price_element = await listing.query_selector("._64if862._194zg6t6")
                price = await price_element.inner_text() if price_element else "N/A"

                # Append the extracted data to house_data list
                house_data.append(
                    {
                        "House_ID": house_id,
                        "Listing_URL": full_url,
                        "Address": address,
                        "Tenure": tenure,
                        "Beds": int(beds.split(" ")[0]) if beds != "N/A" else None,
                        "Baths": int(baths.split(" ")[0]) if baths != "N/A" else None,
                        "Receptions": (
                            int(receptions.split(" ")[0])
                            if receptions != "N/A"
                            else None
                        ),
                        "Price": price,
                    }
                )

                # Increment the house ID
                house_id += 1

            # Increment the page number
            page_number += 1

            await context.close()

        # Write the collected house data to a JSON file
        with open("house_data.json", "w", encoding="utf-8") as f:
            json.dump(house_data, f, ensure_ascii=False, indent=4)

        print("Data saved to 'house_data.json'")

    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
