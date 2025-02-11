import csv
import requests
from datetime import datetime

# File paths
CSV_FILE = "tcg_price_data.csv"
BASE_PRODUCT_API_URL = "https://tcgcsv.com/tcgplayer/3/23821/products"
DETAIL_API_URL = "https://mp-search-api.tcgplayer.com/v2/product/{}/details?mpfev=3151"

def fetch_products():
    """Fetch product data from the product API."""
    response = requests.get(BASE_PRODUCT_API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch product data. HTTP Status: {response.status_code}")
        return []

def fetch_product_details(product_id):
    """Fetch detailed data for a specific product using its ID."""
    response = requests.get(DETAIL_API_URL.format(product_id))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch details for product ID {product_id}. HTTP Status: {response.status_code}")
        return {}

def compare_data(existing_data, new_data):
    """Compare existing data with new data to calculate price changes."""
    if not existing_data:
        return new_data

    try:
        existing_price = float(existing_data["market_price"]) if existing_data["market_price"] else 0.0
    except ValueError:
        existing_price = 0.0
    
    try:
        new_price = float(new_data["market_price"]) if new_data["market_price"] else 0.0
    except ValueError:
        new_price = 0.0
    
    # Calculate price change percentage
    price_change = round(((new_price - existing_price) / existing_price) * 100, 2) if existing_price else 0
    new_data["priceChange"] = f"{price_change}%" if price_change else "N/A"

    # Update latest change time if price has changed
    if existing_price != new_price:
        new_data["latestChange"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        new_data["latestChange"] = existing_data.get("latestChange")

    return new_data

def write_to_csv(data):
    """Write or update product data into a CSV file."""
    headers = [
        "product_id", "name", "imageURL", "url", "num_listings",
        "lowest_price_with_shipping", "market_price", "latestChange", "priceChange"
    ]
    # Read existing data
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            existing_data = {row["product_id"]: row for row in reader}
    except FileNotFoundError:
        existing_data = {}

    # Update data
    updated_data = []
    for product in data:
        product_id = str(product["product_id"])
        existing_row = existing_data.get(product_id, {})
        updated_row = compare_data(existing_row, product)
        updated_data.append(updated_row)

    # Write updated data back to CSV
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_data)

def main():
    # Fetch product list
    products = fetch_products()
    all_product_data = []

    print(f"Fetching data for {len(products)} products...")
    
    for product in products:
        product_id = product["productId"]
        product_details = fetch_product_details(product_id)

        # Extract and format data
        product_data = {
            "product_id": product["productId"],
            "name": product["name"],
            "imageURL": product["imageUrl"],
            "url": product["url"],
            "num_listings": product_details.get("listings", 0),
            "lowest_price_with_shipping": product_details.get("lowestPriceWithShipping", 0.0),
            "market_price": product_details.get("marketPrice", 0.0),
            "latestChange": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priceChange": 0.0
        }
        all_product_data.append(product_data)

    # Write to CSV
    write_to_csv(all_product_data)
    print(f"Price data updated in {CSV_FILE}")

if __name__ == "__main__":
    main()