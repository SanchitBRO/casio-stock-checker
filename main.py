import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.hmtwatches.store/product/b8fbabdb-a49d-4e5d-92c6-71eda34c9382"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Bot credentials not found.")
        return
        
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    try:
        requests.post(send_url, data=payload)
        print("Alert Sent!")
    except Exception as e:
        print(f"Error sending message: {e}")

def check_stock():
    print(f"Checking {URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        if response.status_code != 200:
            print(f"Failed to load page. Status: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()
        
        if "buy now" in page_text:
            # DOUBLE CHECK: Sometimes "Add to cart" is hidden but "Sold out" is visible.
            # We assume if "Add to cart" is readable in the text, it's good.
            print("STATUS: POTENTIALLY IN STOCK!")
            send_telegram_message(
                f"🚨SANCHIT - HMT STOCK ALERT! 🚨\n"
                f"HMT Stellar DASS 04 in STOCK !!\n"
                f"Buy here: {URL}"
            )
        elif "out of stock" in page_text:
            print("STATUS: Sold Out")
        else:
            print("STATUS: Unknown (Keywords not found). The page structure might have changed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_stock()
