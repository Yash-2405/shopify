from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProductInfo(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    handle: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    tags: Optional[List[str]] = None
    price: Optional[str] = None
    compare_at_price: Optional[str] = None
    available: Optional[bool] = None
    images: Optional[List[str]] = None
    variants: Optional[List[Dict[str, Any]]] = None

class ContactDetails(BaseModel):
    emails: Optional[List[str]] = None
    phone_numbers: Optional[List[str]] = None
    address: Optional[str] = None

class SocialHandles(BaseModel):
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    linkedin: Optional[str] = None

class FAQ(BaseModel):
    question: str
    answer: str

class ImportantLinks(BaseModel):
    order_tracking: Optional[str] = None
    contact_us: Optional[str] = None
    blogs: Optional[str] = None
    about_us: Optional[str] = None
    shipping_info: Optional[str] = None

class BrandInsights(BaseModel):
    website_url: str
    brand_name: Optional[str] = None
    product_catalog: Optional[List[ProductInfo]] = None
    hero_products: Optional[List[ProductInfo]] = None
    privacy_policy: Optional[str] = None
    return_refund_policy: Optional[str] = None
    faqs: Optional[List[FAQ]] = None
    social_handles: Optional[SocialHandles] = None
    contact_details: Optional[ContactDetails] = None
    brand_context: Optional[str] = None
    important_links: Optional[ImportantLinks] = None
    additional_data: Optional[Dict[str, Any]] = None
    scraped_at: Optional[datetime] = None
    scraping_status: str = "completed"

class BrandRequest(BaseModel):
    website_url: HttpUrl

class BrandResponse(BaseModel):
    success: bool
    data: Optional[BrandInsights] = None
    error: Optional[str] = None
    status_code: int = 200