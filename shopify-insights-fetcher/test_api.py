import requests
import json

# Test the API endpoints
base_url = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{base_url}/health")
    print("Health Check:", response.json())

def test_root():
    """Test root endpoint"""
    response = requests.get(f"{base_url}/")
    print("Root Endpoint:", response.json())

def test_shopify_scraper():
    """Test Shopify scraper with a real Shopify store"""
    test_data = {
        "website_url": "https://memy.co.in"
    }
    
    response = requests.post(
        f"{base_url}/api/v1/shopify/fetch-insights",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Shopify Scraper Test:")
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        print("Success:", result.get("success"))
        if result.get("data"):
            data = result["data"]
            print("Brand Name:", data.get("brand_name"))
            
            # Safe handling of product catalog
            product_catalog = data.get("product_catalog") or []
            print("Product Count:", len(product_catalog))
            
            # Safe handling of hero products
            hero_products = data.get("hero_products") or []
            print("Hero Products Count:", len(hero_products))
            
            print("Has Privacy Policy:", bool(data.get("privacy_policy")))
            print("Has Return Policy:", bool(data.get("return_refund_policy")))
            print("Has FAQs:", bool(data.get("faqs")))
            print("Has Social Handles:", data.get("social_handles") is not None)
            print("Has Contact Details:", data.get("contact_details") is not None)
            print("Has Brand Context:", bool(data.get("brand_context")))
            print("Has Important Links:", data.get("important_links") is not None)
            
            # Show some sample data if available
            if product_catalog:
                print("\nSample Product:")
                sample_product = product_catalog[0]
                print(f"  - Title: {sample_product.get('title', 'N/A')}")
                print(f"  - Price: {sample_product.get('price', 'N/A')}")
                print(f"  - Vendor: {sample_product.get('vendor', 'N/A')}")
            
            if data.get("social_handles"):
                print("\nSocial Handles Found:")
                social = data["social_handles"]
                for platform, url in social.items():
                    if url:
                        print(f"  - {platform.title()}: {url}")
            
            if data.get("contact_details"):
                print("\nContact Details Found:")
                contact = data["contact_details"]
                if contact.get("emails"):
                    print(f"  - Emails: {', '.join(contact['emails'][:2])}")  # Show first 2
                if contact.get("phone_numbers"):
                    print(f"  - Phones: {', '.join(contact['phone_numbers'][:2])}")  # Show first 2
        else:
            print("Error:", result.get("error"))
    else:
        print("Error Response:", response.text)

if __name__ == "__main__":
    print("Testing Shopify Insights Fetcher API...")
    print("=" * 50)
    
    test_health()
    print("-" * 30)
    
    test_root()
    print("-" * 30)
    
    test_shopify_scraper()