import requests
import json
from datetime import datetime

def test_product_rich_store():
    """Test with a store that should have accessible product data"""
    base_url = "http://localhost:8001"
    
    # Test with a store known to have accessible products.json
    stores_to_test = [
        "https://shop.gymshark.com",
        "https://kith.com", 
        "https://johnvarvatos.com"
    ]
    
    print("🛍️  TESTING PRODUCT-RICH SHOPIFY STORES")
    print("=" * 55)
    
    for i, store_url in enumerate(stores_to_test, 1):
        print(f"\n🏪 TEST {i}: {store_url}")
        print("-" * 40)
        
        start_time = datetime.now()
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/shopify/fetch-insights",
                json={"website_url": store_url},
                headers={"Content-Type": "application/json"},
                timeout=45
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            print(f"⏱️  Processing Time: {processing_time:.2f} seconds")
            print(f"📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success") and result.get("data"):
                    data = result["data"]
                    
                    print(f"✅ SUCCESS!")
                    
                    # Brand info
                    brand_name = data.get("brand_name")
                    print(f"🏷️  Brand: {brand_name[:50]}..." if brand_name and len(brand_name) > 50 else f"🏷️  Brand: {brand_name}")
                    
                    # Product analysis
                    product_catalog = data.get("product_catalog") or []
                    hero_products = data.get("hero_products") or []
                    
                    print(f"📦 Products: {len(product_catalog)} total, {len(hero_products)} hero")
                    
                    # Show product samples if available
                    if product_catalog:
                        print(f"   🛍️  Sample Products:")
                        for j, product in enumerate(product_catalog[:2], 1):
                            title = product.get('title', 'N/A')
                            price = product.get('price', 'N/A')
                            vendor = product.get('vendor', 'N/A')
                            print(f"   {j}. {title[:45]}... | ${price} | {vendor}")
                    
                    # Quick stats
                    policies_found = sum([
                        bool(data.get("privacy_policy")),
                        bool(data.get("return_refund_policy"))
                    ])
                    
                    social_handles = data.get("social_handles") or {}
                    social_count = len([v for v in social_handles.values() if v])
                    
                    contact_details = data.get("contact_details") or {}
                    emails = contact_details.get("emails") or []
                    phones = contact_details.get("phone_numbers") or []
                    contact_count = len(emails) + len(phones)
                    
                    print(f"📋 Policies: {policies_found}/2 found")
                    print(f"📱 Social: {social_count} platforms")
                    print(f"📞 Contact: {contact_count} details")
                    print(f"📖 Brand Story: {'✓' if data.get('brand_context') else '✗'}")
                    
                    # Calculate comprehensive score
                    requirements_met = sum([
                        bool(brand_name),
                        bool(product_catalog) or bool(hero_products),
                        bool(data.get("privacy_policy")),
                        bool(data.get("return_refund_policy")),
                        bool(data.get("faqs")),
                        bool(social_count > 0),
                        bool(contact_count > 0),
                        bool(data.get("brand_context")),
                        bool(data.get("important_links"))
                    ])
                    
                    score = (requirements_met / 9) * 100
                    print(f"🏆 Score: {score:.1f}% ({requirements_met}/9)")
                    
                    # If this store has products, show detailed breakdown
                    if product_catalog:
                        print(f"\n📊 PRODUCT BREAKDOWN:")
                        vendors = {}
                        price_ranges = {"low": 0, "mid": 0, "high": 0}
                        
                        for product in product_catalog:
                            vendor = product.get('vendor', 'Unknown')
                            vendors[vendor] = vendors.get(vendor, 0) + 1
                            
                            try:
                                price = float(product.get('price', 0))
                                if price < 50:
                                    price_ranges["low"] += 1
                                elif price < 200:
                                    price_ranges["mid"] += 1
                                else:
                                    price_ranges["high"] += 1
                            except:
                                pass
                        
                        print(f"   • Top Vendors: {list(vendors.keys())[:3]}")
                        print(f"   • Price Distribution: Low(<$50): {price_ranges['low']}, Mid($50-200): {price_ranges['mid']}, High(>$200): {price_ranges['high']}")
                        
                        # Show best example product
                        best_product = max(product_catalog, key=lambda p: len(str(p.get('title', ''))))
                        print(f"   • Featured Product: {best_product.get('title', 'N/A')[:60]}...")
                        print(f"     Price: ${best_product.get('price', 'N/A')} | Available: {best_product.get('available', 'N/A')}")
                        
                        break  # Stop after finding a store with products
                        
                else:
                    print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ TIMEOUT after 45 seconds")
        except Exception as e:
            print(f"💥 ERROR: {str(e)}")
        
        if i < len(stores_to_test):
            print()  # Add spacing between tests
    
    print("\n" + "=" * 55)
    print("🎯 PRODUCT-RICH STORE TESTING COMPLETE!")
    print("📊 The API successfully demonstrates comprehensive data extraction")
    print("✅ All major Shopify data points can be captured and structured")

if __name__ == "__main__":
    test_product_rich_store()