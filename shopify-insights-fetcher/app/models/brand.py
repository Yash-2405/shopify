from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String(500), unique=True, index=True, nullable=False)
    brand_name = Column(String(255), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Brand insights
    product_catalog = Column(JSON, nullable=True)
    hero_products = Column(JSON, nullable=True)
    privacy_policy = Column(Text, nullable=True)
    return_refund_policy = Column(Text, nullable=True)
    faqs = Column(JSON, nullable=True)
    social_handles = Column(JSON, nullable=True)
    contact_details = Column(JSON, nullable=True)
    brand_context = Column(Text, nullable=True)
    important_links = Column(JSON, nullable=True)
    
    # Additional insights
    additional_data = Column(JSON, nullable=True)
    
    # Metadata
    scraping_status = Column(String(50), default="pending")  # pending, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Bonus features
    competitors = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)