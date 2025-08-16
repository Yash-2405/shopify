import requests
import json
from datetime import datetime

def test_specific_shopify_store():
    """Test API with a specific well-known Shopify store"""
    base_url = "http://localhost:8001"
    
    # Test with Allbirds - a famous Shopify success story
    store_url = "https://allbirds.com"
    
    print("🎯 TESTING SPECIFIC SHOPIFY STORE")
    print("=" * 50)
    print(f"🏪 Store: {store_url}")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    start_time = datetime.now()
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/shopify/fetch-insights",
            json={"website_url": store_url},
            headers={"Content-Type": "application/json"},
            timeout=60  # Extended timeout for comprehensive scraping
        )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"⏱️  Processing Time: {processing_time:.2f} seconds")
        print(f"📡 HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                print("\n✅ SUCCESS - COMPREHENSIVE DATA EXTRACTED!")
                print("=" * 50)
                
                # Brand Information
                brand_name = data.get("brand_name")
                print(f"🏷️  Brand Name: {brand_name if brand_name else 'Not found'}")
                
                # Product Catalog Analysis
                product_catalog = data.get("product_catalog") or []
                hero_products = data.get("hero_products") or []
                
                print(f"\n📦 PRODUCT INFORMATION:")
                print(f"   • Total Products: {len(product_catalog)}")
                print(f"   • Hero Products: {len(hero_products)}")
                
                if product_catalog:
                    print(f"\n   📝 Sample Products (first 3):")
                    for i, product in enumerate(product_catalog[:3], 1):
                        title = product.get('title', 'N/A')
                        price = product.get('price', 'N/A')
                        vendor = product.get('vendor', 'N/A')
                        available = product.get('available', 'N/A')
                        print(f"   {i}. {title[:60]}...")
                        print(f"      Price: ${price} | Vendor: {vendor} | Available: {available}")
                
                # Policy Information
                privacy_policy = data.get("privacy_policy")
                return_policy = data.get("return_refund_policy")
                
                print(f"\n📋 POLICY INFORMATION:")
                print(f"   • Privacy Policy: {'✓ Found' if privacy_policy else '✗ Not found'}")
                if privacy_policy:
                    print(f"     Length: {len(privacy_policy)} characters")
                    print(f"     Preview: {privacy_policy[:150]}...")
                
                print(f"   • Return/Refund Policy: {'✓ Found' if return_policy else '✗ Not found'}")
                if return_policy:
                    print(f"     Length: {len(return_policy)} characters")
                    print(f"     Preview: {return_policy[:150]}...")
                
                # FAQ Information
                faqs = data.get("faqs") or []
                print(f"\n❓ FAQ INFORMATION:")
                print(f"   • Total FAQs: {len(faqs)}")
                if faqs:
                    print(f"   📝 Sample FAQs (first 2):")
                    for i, faq in enumerate(faqs[:2], 1):
                        question = faq.get('question', 'N/A')
                        answer = faq.get('answer', 'N/A')
                        print(f"   {i}. Q: {question[:80]}...")
                        print(f"      A: {answer[:80]}...")
                
                # Social Media Analysis
                social_handles = data.get("social_handles") or {}
                print(f"\n📱 SOCIAL MEDIA HANDLES:")
                social_count = len([v for v in social_handles.values() if v])
                print(f"   • Platforms Found: {social_count}")
                
                for platform, url in social_handles.items():
                    if url:
                        print(f"   • {platform.title()}: {url}")
                
                # Contact Information
                contact_details = data.get("contact_details") or {}
                emails = contact_details.get("emails") or []
                phones = contact_details.get("phone_numbers") or []
                addresses = contact_details.get("addresses") or []
                
                print(f"\n📞 CONTACT INFORMATION:")
                print(f"   • Emails Found: {len(emails)}")
                for email in emails[:3]:  # Show first 3
                    print(f"     - {email}")
                
                print(f"   • Phone Numbers Found: {len(phones)}")
                for phone in phones[:3]:  # Show first 3
                    print(f"     - {phone}")
                
                print(f"   • Addresses Found: {len(addresses)}")
                for address in addresses[:2]:  # Show first 2
                    print(f"     - {address}")
                
                # Brand Context
                brand_context = data.get("brand_context")
                print(f"\n📖 BRAND CONTEXT:")
                print(f"   • Brand Story: {'✓ Found' if brand_context else '✗ Not found'}")
                if brand_context:
                    print(f"     Length: {len(brand_context)} characters")
                    print(f"     Preview: {brand_context[:200]}...")
                
                # Important Links
                important_links = data.get("important_links") or {}
                print(f"\n🔗 IMPORTANT LINKS:")
                link_count = len([v for v in important_links.values() if v])
                print(f"   • Links Found: {link_count}")
                
                for link_type, url in important_links.items():
                    if url:
                        print(f"   • {link_type.replace('_', ' ').title()}: {url}")
                
                # Scraping Status
                scraping_status = data.get("scraping_status", "unknown")
                scraped_at = data.get("scraped_at", "N/A")
                
                print(f"\n📊 SCRAPING METADATA:")
                print(f"   • Status: {scraping_status}")
                print(f"   • Scraped At: {scraped_at}")
                
                # Summary
                print(f"\n🎯 EXTRACTION SUMMARY:")
                print(f"   • Brand Name: {'✓' if brand_name else '✗'}")
                print(f"   • Products: {'✓' if product_catalog else '✗'} ({len(product_catalog)} found)")
                print(f"   • Hero Products: {'✓' if hero_products else '✗'} ({len(hero_products)} found)")
                print(f"   • Privacy Policy: {'✓' if privacy_policy else '✗'}")
                print(f"   • Return Policy: {'✓' if return_policy else '✗'}")
                print(f"   • FAQs: {'✓' if faqs else '✗'} ({len(faqs)} found)")
                print(f"   • Social Media: {'✓' if social_count > 0 else '✗'} ({social_count} platforms)")
                print(f"   • Contact Info: {'✓' if emails or phones or addresses else '✗'}")
                print(f"   • Brand Story: {'✓' if brand_context else '✗'}")
                print(f"   • Important Links: {'✓' if link_count > 0 else '✗'} ({link_count} found)")
                
                # Calculate success rate
                requirements = [
                    bool(brand_name),
                    bool(product_catalog) or bool(hero_products),
                    bool(privacy_policy),
                    bool(return_policy),
                    bool(faqs),
                    bool(social_count > 0),
                    bool(emails or phones or addresses),
                    bool(brand_context),
                    bool(link_count > 0)
                ]
                
                success_rate = (sum(requirements) / len(requirements)) * 100
                print(f"\n🏆 SUCCESS RATE: {success_rate:.1f}% ({sum(requirements)}/9 requirements met)")
                
            else:
                print(f"\n❌ SCRAPING FAILED")
                print(f"Error: {result.get('error', 'Unknown error occurred')}")
                
        else:
            print(f"\n❌ HTTP ERROR")
            print(f"Status Code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error Details: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}...")
                
    except requests.exceptions.Timeout:
        print(f"\n⏰ REQUEST TIMEOUT")
        print("The request took longer than 60 seconds to complete.")
        
    except requests.exceptions.ConnectionError:
        print(f"\n🔌 CONNECTION ERROR")
        print("Could not connect to the API server.")
        
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR")
        print(f"Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 SPECIFIC STORE TEST COMPLETE!")

if __name__ == "__main__":
    test_specific_shopify_store()