from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import asyncio
from app.schemas.brand import BrandRequest, BrandResponse, BrandInsights
from app.services.shopify_scraper import ShopifyScraper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/fetch-insights", response_model=BrandResponse)
async def fetch_brand_insights(request: BrandRequest) -> BrandResponse:
    """
    Fetch brand insights from a Shopify store URL
    
    Args:
        request: BrandRequest containing website_url
        
    Returns:
        BrandResponse with scraped insights or error information
    """
    try:
        website_url = str(request.website_url)
        logger.info(f"Starting to scrape insights for: {website_url}")
        
        # Initialize scraper
        scraper = ShopifyScraper()
        
        # Scrape brand insights
        insights = await scraper.scrape_brand_insights(website_url)
        
        logger.info(f"Successfully scraped insights for: {website_url}")
        
        return BrandResponse(
            success=True,
            data=insights,
            status_code=200
        )
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error scraping {website_url}: {error_message}")
        
        # Determine appropriate status code
        status_code = 500
        if "not found" in error_message.lower() or "404" in error_message:
            status_code = 404
        elif "timeout" in error_message.lower():
            status_code = 408
        elif "connection" in error_message.lower():
            status_code = 503
            
        return BrandResponse(
            success=False,
            error=error_message,
            status_code=status_code
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the Shopify scraper service"""
    return {"status": "healthy", "service": "shopify-scraper"}

@router.get("/test-scraper/{test_url:path}")
async def test_scraper(test_url: str) -> Dict[str, Any]:
    """
    Test endpoint to quickly check if a URL is scrapable
    
    Args:
        test_url: URL to test (without protocol)
        
    Returns:
        Basic connectivity and structure information
    """
    try:
        if not test_url.startswith(('http://', 'https://')):
            test_url = 'https://' + test_url
            
        scraper = ShopifyScraper()
        
        # Quick test - just try to get basic info
        brand_name = await scraper._get_brand_name(test_url)
        product_catalog = await scraper._get_product_catalog(test_url)
        
        return {
            "url": test_url,
            "accessible": True,
            "brand_name": brand_name,
            "has_products_json": product_catalog is not None,
            "product_count": len(product_catalog) if product_catalog else 0
        }
        
    except Exception as e:
        return {
            "url": test_url,
            "accessible": False,
            "error": str(e)
        }