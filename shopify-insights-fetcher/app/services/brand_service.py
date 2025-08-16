from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.brand import Brand
from app.schemas.brand import BrandInsights
from datetime import datetime
import json

class BrandService:
    """Service for managing brand data in database"""
    
    @staticmethod
    def create_brand_record(db: Session, insights: BrandInsights) -> Brand:
        """Create a new brand record in database"""
        
        # Convert Pydantic models to JSON-serializable dicts
        product_catalog_json = None
        if insights.product_catalog:
            product_catalog_json = [product.dict() for product in insights.product_catalog]
            
        hero_products_json = None
        if insights.hero_products:
            hero_products_json = [product.dict() for product in insights.hero_products]
            
        faqs_json = None
        if insights.faqs:
            faqs_json = [faq.dict() for faq in insights.faqs]
            
        social_handles_json = None
        if insights.social_handles:
            social_handles_json = insights.social_handles.dict()
            
        contact_details_json = None
        if insights.contact_details:
            contact_details_json = insights.contact_details.dict()
            
        important_links_json = None
        if insights.important_links:
            important_links_json = insights.important_links.dict()
        
        db_brand = Brand(
            website_url=insights.website_url,
            brand_name=insights.brand_name,
            product_catalog=product_catalog_json,
            hero_products=hero_products_json,
            privacy_policy=insights.privacy_policy,
            return_refund_policy=insights.return_refund_policy,
            faqs=faqs_json,
            social_handles=social_handles_json,
            contact_details=contact_details_json,
            brand_context=insights.brand_context,
            important_links=important_links_json,
            additional_data=insights.additional_data,
            scraping_status=insights.scraping_status,
            scraped_at=datetime.utcnow()
        )
        
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        
        return db_brand
    
    @staticmethod
    def get_brand_by_url(db: Session, website_url: str) -> Optional[Brand]:
        """Get brand record by website URL"""
        return db.query(Brand).filter(Brand.website_url == website_url).first()
    
    @staticmethod
    def get_all_brands(db: Session, skip: int = 0, limit: int = 100) -> List[Brand]:
        """Get all brand records with pagination"""
        return db.query(Brand).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_brand_record(db: Session, brand_id: int, insights: BrandInsights) -> Optional[Brand]:
        """Update existing brand record"""
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        
        if db_brand:
            # Update fields
            db_brand.brand_name = insights.brand_name
            db_brand.scraped_at = datetime.utcnow()
            db_brand.scraping_status = insights.scraping_status
            
            # Update JSON fields
            if insights.product_catalog:
                db_brand.product_catalog = [product.dict() for product in insights.product_catalog]
            if insights.hero_products:
                db_brand.hero_products = [product.dict() for product in insights.hero_products]
            if insights.faqs:
                db_brand.faqs = [faq.dict() for faq in insights.faqs]
            if insights.social_handles:
                db_brand.social_handles = insights.social_handles.dict()
            if insights.contact_details:
                db_brand.contact_details = insights.contact_details.dict()
            if insights.important_links:
                db_brand.important_links = insights.important_links.dict()
                
            db_brand.privacy_policy = insights.privacy_policy
            db_brand.return_refund_policy = insights.return_refund_policy
            db_brand.brand_context = insights.brand_context
            db_brand.additional_data = insights.additional_data
            
            db.commit()
            db.refresh(db_brand)
            
        return db_brand
    
    @staticmethod
    def delete_brand_record(db: Session, brand_id: int) -> bool:
        """Delete brand record"""
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        
        if db_brand:
            db.delete(db_brand)
            db.commit()
            return True
            
        return False